// === Endless 🌊✨ Tools UI Helper ===

const endlessToolsRegistry = [];

export function registerEndlessTool(name, callback) {
    endlessToolsRegistry.push({ name, callback });
}

export function injectEndlessToolsButton() {
    const toolbar = findToolbar();
    if (!toolbar || document.getElementById("endless-tools-button")) return;

    const btn = document.createElement("button");
    btn.id = "endless-tools-button";
    btn.textContent = "Endless 🌊✨ Tools";
    btn.className = "comfyui-button";
    btn.style.marginLeft = "8px";
    btn.onclick = showEndlessToolMenu;
    toolbar.appendChild(btn);
}

export function showEndlessToolMenu() {
    document.getElementById("endless-tools-float")?.remove();

    const colors = getComfyUIColors();

    const menu = document.createElement("div");
    menu.id = "endless-tools-float";
    menu.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${colors.menu};
        color: ${colors.inputText};
        padding: 12px;
        border: 1px solid ${colors.accent};
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
        z-index: 99999;
        opacity: 1;
        width: fit-content;
        transition: opacity 0.2s ease;
    `;

    const dragBar = document.createElement("div");
    dragBar.textContent = "Endless 🌊✨ Tools Drag Bar";
    dragBar.style.cssText = `
        padding: 4px;
        background: ${toRGBA(colors.inputText, 0.05)};
        cursor: move;
        font-size: 12px;
        text-align: center;
        user-select: none;
        border-bottom: 1px solid ${colors.border};
    `;
    menu.appendChild(dragBar);

    endlessToolsRegistry.sort((a, b) => a.name.localeCompare(b.name)).forEach(tool => {
        const btn = document.createElement("div");
        btn.textContent = `🌊✨ ${tool.name}`;
        btn.style.cssText = `
            padding: 6px 10px;
            cursor: pointer;
            border-radius: 4px;
            transition: background 0.2s ease;
        `;
        btn.onmouseover = () => btn.style.background = toRGBA(colors.inputText, 0.1);
        btn.onmouseout = () => btn.style.background = "transparent";
        btn.onclick = () => {
            tool.callback();
            menu.remove();
        };
        menu.appendChild(btn);
    });

    makeDraggable(menu, dragBar);

    // Live theme updater
    function updateMenuTheme(newColors = getComfyUIColors()) {
        menu.style.background = newColors.menu;
        menu.style.color = newColors.inputText;
        menu.style.borderColor = newColors.accent;
        menu.style.boxShadow = newColors.shadow;
        dragBar.style.background = toRGBA(newColors.inputText, 0.05);
        dragBar.style.borderBottomColor = newColors.border;
    }

    const unregister = onThemeChange(updateMenuTheme);
    menu.remove = ((orig => function () {
        unregister();
        orig.call(this);
    })(menu.remove));

    document.body.appendChild(menu);
}

// === Hotkeys ===
document.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.altKey && e.key.toLowerCase() === 'e') {
        showEndlessToolMenu();
        e.preventDefault();
    }
    if (e.key === "Escape") {
        document.getElementById("endless-tools-float")?.remove();
    }
});

console.log("Endless 🌊✨ Tools menu: press Ctrl+Alt+E if toolbar button is missing.");

function waitForToolbarAndInject() {
    if (document.querySelector('.comfyui-menu')) {
        injectEndlessToolsButton();
        return;
    }
    const observer = new MutationObserver(() => {
        if (document.querySelector('.comfyui-menu')) {
            injectEndlessToolsButton();
            observer.disconnect();
        }
    });
    observer.observe(document.body, { childList: true, subtree: true });
}
waitForToolbarAndInject();

function findToolbar() {
    return (
        document.querySelector('.comfyui-menu, .comfy-menu, [class*="menu"], [class*="toolbar"]') ||
        Array.from(document.querySelectorAll('[class*="button-group"], [class*="btn-group"], .comfyui-button-group'))
            .find(g => g.querySelectorAll('button').length > 0) ||
        Array.from(document.querySelectorAll('*'))
            .find(el => {
                const buttons = el.querySelectorAll('button');
                return buttons.length >= 2 && buttons.length <= 10;
            }) ||
        Array.from(document.querySelectorAll(".comfyui-button-group"))
            .find(div => Array.from(div.querySelectorAll("button")).some(btn => btn.title === "Share"))
    );
}

// === Live Theme Monitoring ===
let themeObserver = null;
const themeCallbacks = new Set();

export function onThemeChange(callback) {
    themeCallbacks.add(callback);
    if (themeCallbacks.size === 1) startThemeObserver();
    return () => {
        themeCallbacks.delete(callback);
        if (themeCallbacks.size === 0) stopThemeObserver();
    };
}

function startThemeObserver() {
    if (themeObserver) return;
    themeObserver = new MutationObserver(() => {
        clearTimeout(window.themeChangeTimeout);
        window.themeChangeTimeout = setTimeout(() => {
            const newColors = getComfyUIColors();
            themeCallbacks.forEach(cb => cb(newColors));
        }, 100);
    });
    themeObserver.observe(document.documentElement, { attributes: true, attributeFilter: ['class', 'style', 'data-theme'] });
    themeObserver.observe(document.body, { attributes: true, attributeFilter: ['class', 'style', 'data-theme'] });
}

function stopThemeObserver() {
    if (themeObserver) {
        themeObserver.disconnect();
        themeObserver = null;
    }
}

export function getComfyUIColors() {
    const computed = getComputedStyle(document.documentElement);
    const getVar = name => computed.getPropertyValue(name).trim() || null;
    return {
        fg: getVar("--fg-color") || "#ddd",
        bg: getVar("--bg-color") || "#353535",
        menu: getVar("--comfy-menu-bg") || "#353535",
        menuSecondary: getVar("--comfy-menu-secondary-bg") || "#222",
        inputBg: getVar("--comfy-input-bg") || "#222",
        inputText: getVar("--input-text") || "#ddd",
        descriptionText: getVar("--descrip-text") || "#999",
        dragText: getVar("--drag-text") || "#ddd",
        errorText: getVar("--error-text") || "#f44336",
        border: getVar("--border-color") || "#999",
        accent: getVar("--comfy-accent") || getVar("--comfy-accent-color") || "#4a90e2",
        hoverBg: getVar("--content-hover-bg") || "rgba(255,255,255,0.1)",
        hoverFg: getVar("--content-hover-fg") || "#fff",
        shadow: getVar("--bar-shadow") || "0 2px 10px rgba(0,0,0,0.3)",
        dialogBg: getVar("--comfy-menu-bg") || getVar("--bg-color") || "#353535",
        buttonHoverBg: getVar("--content-hover-bg") || "rgba(255,255,255,0.1)"
    };
}

export function toRGBA(color, alpha = 0.2) {
    if (!color) return `rgba(128,128,128,${alpha})`;
    color = color.trim();
    if (color.startsWith('#')) {
        const hex = color.slice(1);
        const fullHex = hex.length === 3 ? hex.split('').map(c => c + c).join('') : hex;
        const bigint = parseInt(fullHex, 16);
        const r = (bigint >> 16) & 255, g = (bigint >> 8) & 255, b = bigint & 255;
        return `rgba(${r}, ${g}, ${b}, ${alpha})`;
    }
    if (color.startsWith('rgb')) {
        const rgb = color.match(/\d+/g);
        if (rgb?.length >= 3) return `rgba(${rgb[0]}, ${rgb[1]}, ${rgb[2]}, ${alpha})`;
    }
    return `rgba(128,128,128,${alpha})`;
}

export function blendColors(color1, color2, ratio) {
    const c1 = toRGBA(color1, 1).match(/\d+/g);
    const c2 = toRGBA(color2, 1).match(/\d+/g);
    if (!c1 || !c2) return color1;
    const r = Math.round(c1[0] * (1 - ratio) + c2[0] * ratio);
    const g = Math.round(c1[1] * (1 - ratio) + c2[1] * ratio);
    const b = Math.round(c1[2] * (1 - ratio) + c2[2] * ratio);
    return `rgb(${r}, ${g}, ${b})`;
}

export function addButtonHoverEffects(container) {
    container?.querySelectorAll('button').forEach(button => {
        button.addEventListener('mouseenter', () => {
            button.style.boxShadow = '0 0 0 1px currentColor';
            button.style.filter = 'brightness(1.1)';
            button.style.transform = 'translateY(-1px)';
        });
        button.addEventListener('mouseleave', () => {
            button.style.boxShadow = 'none';
            button.style.filter = 'brightness(1)';
            button.style.transform = 'translateY(0px)';
        });
    });
}

export function makeDraggable(element, handle = element) {
    let offsetX = 0, offsetY = 0, isDown = false;
    handle.onmousedown = (e) => {
        isDown = true;
        if (element.style.position !== 'fixed') {
            element.style.position = 'fixed';
            element.style.right = 'auto';
        }
        const rect = element.getBoundingClientRect();
        offsetX = e.clientX - rect.left;
        offsetY = e.clientY - rect.top;
        element.style.cursor = 'move';
        document.onmousemove = (e) => {
            if (!isDown) return;
            element.style.left = `${e.clientX - offsetX}px`;
            element.style.top = `${e.clientY - offsetY}px`;
            element.style.transform = 'none';
        };
        document.onmouseup = () => {
            isDown = false;
            element.style.cursor = 'default';
            document.onmousemove = null;
            document.onmouseup = null;
        };
    };
}

// === Global exposure for F12 ===
window.EndlessHelpers = {
    registerEndlessTool,
    injectEndlessToolsButton,
    showEndlessToolMenu,
    onThemeChange,
    getComfyUIColors,
    toRGBA,
    blendColors,
    addButtonHoverEffects,
    makeDraggable
};
