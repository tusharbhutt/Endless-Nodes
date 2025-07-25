// ComfyUI Endless 🌊✨ Fontifier - Fully Fixed Version

(function waitForHelpers() {
    if (typeof window.EndlessHelpers === 'undefined') {
        console.warn("⏳ Waiting for EndlessHelpers to be ready...");
        setTimeout(waitForHelpers, 100); // Retry every 100ms
        return;
    }

    // Load helpers from window
    const {
        registerEndlessTool,
        injectEndlessToolsButton,
        showEndlessToolMenu,
        onThemeChange,
        getComfyUIColors,
        toRGBA,
        blendColors,
        addButtonHoverEffects,
        makeDraggable
    } = window.EndlessHelpers;

    // === ORIGINAL COMFYUI DEFAULTS ===
    const originalValues = {
        NODE_TEXT_SIZE: LiteGraph.NODE_TEXT_SIZE || 14,
        NODE_SUBTEXT_SIZE: LiteGraph.NODE_SUBTEXT_SIZE || 12,
        NODE_TITLE_HEIGHT: LiteGraph.NODE_TITLE_HEIGHT || 30,
        DEFAULT_GROUP_FONT: LiteGraph.DEFAULT_GROUP_FONT || 24,
        NODE_FONT: LiteGraph.NODE_FONT || 'Arial',
        NODE_SLOT_HEIGHT: LiteGraph.NODE_SLOT_HEIGHT || 20,
        NODE_WIDGET_HEIGHT: LiteGraph.NODE_WIDGET_HEIGHT || 20,
        WIDGET_TEXT_SIZE: 12,
        GLOBAL_SCALE: 1
    };

    const saved = localStorage.getItem("endless_fontifier_defaults");
    let currentValues = saved ? JSON.parse(saved) : { ...originalValues };
    let dialogOpenValues = null;
    let currentDialog = null;
    let handlersSetup = false;
    let escHandler = null;
    let unregisterThemeCallback = null;
    let isPreviewMode = false;

    function createFontifierDialog() {
        if (currentDialog) return;

        const colors = getComfyUIColors();

        const dialog = document.createElement("div");
        dialog.id = "fontifier-dialog";
        dialog.style.cssText = `
            position: absolute;
            z-index: 9999;
            top: 100px;
            left: 100px;
            width: 320px;
            background: ${colors.dialogBg || colors.menu || 'rgba(20, 20, 20, 0.95)'};
            color: ${colors.inputText || '#fff'};
            font-family: sans-serif;
            border: 1px solid ${colors.border};
            border-radius: 10px;
            box-shadow: ${colors.shadow || '0 0 20px rgba(0,0,0,0.5)'};
            padding: 10px;
        `;

        // Clean up any existing style tags
        const existingStyle = document.getElementById('fontifier-dialog-style');
        if (existingStyle) existingStyle.remove();

        // Themed style block
        const style = document.createElement("style");
        style.id = "fontifier-dialog-style";
        style.textContent = createStyleCSS(colors);
        document.head.appendChild(style);

        dialog.innerHTML = `
            <div id="drag-bar" style="text-align:center; padding:6px; background:${colors.menuSecondary || '#2a2a2a'}; cursor:move; border-radius:10px 10px 0 0;">Endless 🌊✨ Drag Bar</div>
            <h2 style="margin: 8px 0; text-align: center;">Fontifier Settings</h2>

            <div class="fontifier-setting">
                <label>Global Scale</label>
                <div class="fontifier-row">
                    <input type="range" id="global-scale" min="0.5" max="2" step="0.01" value="1" title="Overall scaling factor for all font sizes">
                    <input type="number" id="global-scale-num" min="0.5" max="2" step="0.01" value="1" title="Overall scaling factor for all font sizes">
                </div>
            </div>

            <div class="fontifier-setting">
                <label>Text Size</label>
                <div class="fontifier-row">
                    <input type="range" id="node-text-size" min="8" max="32" value="14" title="Font size for node text content and labels">
                    <input type="number" id="node-text-size-num" min="8" max="32" value="14" title="Font size for node text content and labels">
                </div>
            </div>

            <div class="fontifier-setting">
                <label>Subtext Size</label>
                <div class="fontifier-row">
                    <input type="range" id="node-subtext-size" min="8" max="32" value="12" title="Font size for secondary text and descriptions">
                    <input type="number" id="node-subtext-size-num" min="8" max="32" value="12" title="Font size for secondary text and descriptions">
                </div>
            </div>

            <div class="fontifier-setting">
                <label>Title Height</label>
                <div class="fontifier-row">
                    <input type="range" id="title-height" min="20" max="60" value="30" title="Height of node title bars">
                    <input type="number" id="title-height-num" min="20" max="60" value="30" title="Height of node title bars">
                </div>
            </div>

            <div class="fontifier-setting">
                <label>Slot Height</label>
                <div class="fontifier-row">
                    <input type="range" id="slot-height" min="10" max="40" value="20" title="Height of input/output connection slots">
                    <input type="number" id="slot-height-num" min="10" max="40" value="20" title="Height of input/output connection slots">
                </div>
            </div>

            <div class="fontifier-setting">
                <label>Group Font Size</label>
                <div class="fontifier-row">
                    <input type="range" id="group-font-size" min="8" max="32" value="24" title="Font size for group labels and titles">
                    <input type="number" id="group-font-size-num" min="8" max="32" value="24" title="Font size for group labels and titles">
                </div>
            </div>

            <div class="fontifier-setting">
                <label>Widget Font Size</label>
                <div class="fontifier-row">
                    <input type="range" id="widget-text-size" min="8" max="32" value="12" title="Font size for input widgets and controls">
                    <input type="number" id="widget-text-size-num" min="8" max="32" value="12" title="Font size for input widgets and controls">
                </div>
            </div>

            <div class="fontifier-setting">
                <label>Font Family</label>
                <select id="font-family" style="width: 100%;" title="Choose the font family for all text elements">
                    <option value="Arial">Arial</option>
                    <option value="Verdana">Verdana</option>
                    <option value="Tahoma">Tahoma</option>
                    <option value="Courier New">Courier New</option>
                    <option value="Georgia">Georgia</option>
                </select>
            </div>

            <div id="preview-indicator" style="display: none; text-align: center; color: ${colors.accent}; font-size: 12px; margin: 8px 0;">
                🔍 Preview Mode - Changes not saved
            </div>

            <div style="margin-top: 12px; display: flex; flex-wrap: wrap; gap: 6px; justify-content: space-between;">
                <button id="apply-btn" title="Apply changes permanently and close dialog">Apply</button>
                <button id="preview-btn" title="Preview changes temporarily without saving">Preview</button>
                <button id="reset-btn" title="Reset to ComfyUI defaults">Reset</button>
                <button id="save-defaults-btn" title="Save current settings as defaults">💾 Save as Default</button>
                <button id="cancel-btn" title="Cancel changes and close dialog">Cancel</button>
            </div>
        `;

        document.body.appendChild(dialog);
        makeDraggable(dialog, dialog.querySelector('#drag-bar'));
        setupDialogHandlers(dialog);
        currentDialog = dialog;
        
        // Store the values when dialog opens for cancel functionality
        dialogOpenValues = { ...currentValues };
        
        // Set current values in the dialog
        updateDialogValues(dialog);

        // Live theme updating without closing dialog
        unregisterThemeCallback = onThemeChange(() => {
            if (currentDialog) {
                updateDialogTheme();
            }
        });
    }

    function createStyleCSS(colors) {
        return `
            .fontifier-setting {
                margin-bottom: 10px;
            }
            .fontifier-row {
                display: flex;
                align-items: center;
                gap: 6px;
            }
            .fontifier-row input[type="range"] {
                flex-grow: 1;
            }
            .fontifier-row input[type="number"] {
                width: 50px;
                background: ${colors.inputBg || '#222'};
                border: 1px solid ${colors.border || '#999'};
                color: ${colors.inputText || '#ddd'};
                border-radius: 4px;
                padding: 2px;
            }
            #fontifier-dialog button {
                flex-grow: 1;
                padding: 6px;
                background: ${colors.inputBg || '#222'};
                border: 1px solid ${colors.border || '#999'};
                color: ${colors.inputText || '#ddd'};
                border-radius: 4px;
                cursor: pointer;
            }
            #fontifier-dialog button:hover {
                background: ${colors.buttonHoverBg || colors.hoverBg || blendColors(colors.inputBg || '#222', '#ffffff', 0.1)};
            }
            #fontifier-dialog #apply-btn {
                background: ${toRGBA(colors.accent || '#4CAF50', 0.3)};
                border-color: ${colors.accent || '#4CAF50'};
            }
            #fontifier-dialog #cancel-btn {
                background: ${toRGBA(colors.errorText || '#f44336', 0.3)};
                border-color: ${colors.errorText || '#f44336'};
            }
            #fontifier-dialog select {
                background: ${colors.inputBg || '#222'};
                border: 1px solid ${colors.border || '#999'};
                color: ${colors.inputText || '#ddd'};
                border-radius: 4px;
                padding: 4px;
            }
        `;
    }

    function updateDialogTheme() {
        if (!currentDialog) return;
        
        const newColors = getComfyUIColors();
        
        // Update main dialog styling
        currentDialog.style.background = newColors.dialogBg || newColors.menu || 'rgba(20, 20, 20, 0.95)';
        currentDialog.style.color = newColors.inputText || '#fff';
        currentDialog.style.borderColor = newColors.border || '#999';
        currentDialog.style.boxShadow = newColors.shadow || '0 0 20px rgba(0,0,0,0.5)';
        
        // Update drag bar
        const dragBar = currentDialog.querySelector('#drag-bar');
        if (dragBar) {
            dragBar.style.background = newColors.menuSecondary || '#2a2a2a';
        }
        
        // Update preview indicator
        const previewIndicator = currentDialog.querySelector('#preview-indicator');
        if (previewIndicator) {
            previewIndicator.style.color = newColors.accent || '#4CAF50';
        }
        
        // Update the style tag with new colors
        const styleTag = document.getElementById('fontifier-dialog-style');
        if (styleTag) {
            styleTag.textContent = createStyleCSS(newColors);
        }
    }

    function updateDialogValues(dialog) {
        dialog.querySelector('#global-scale').value = currentValues.GLOBAL_SCALE || 1;
        dialog.querySelector('#global-scale-num').value = currentValues.GLOBAL_SCALE || 1;
        dialog.querySelector('#node-text-size').value = currentValues.NODE_TEXT_SIZE;
        dialog.querySelector('#node-text-size-num').value = currentValues.NODE_TEXT_SIZE;
        dialog.querySelector('#node-subtext-size').value = currentValues.NODE_SUBTEXT_SIZE;
        dialog.querySelector('#node-subtext-size-num').value = currentValues.NODE_SUBTEXT_SIZE;
        dialog.querySelector('#title-height').value = currentValues.NODE_TITLE_HEIGHT;
        dialog.querySelector('#title-height-num').value = currentValues.NODE_TITLE_HEIGHT;
        dialog.querySelector('#slot-height').value = currentValues.NODE_SLOT_HEIGHT;
        dialog.querySelector('#slot-height-num').value = currentValues.NODE_SLOT_HEIGHT;
        dialog.querySelector('#group-font-size').value = currentValues.DEFAULT_GROUP_FONT;
        dialog.querySelector('#group-font-size-num').value = currentValues.DEFAULT_GROUP_FONT;
        dialog.querySelector('#widget-text-size').value = currentValues.WIDGET_TEXT_SIZE;
        dialog.querySelector('#widget-text-size-num').value = currentValues.WIDGET_TEXT_SIZE;
        dialog.querySelector('#font-family').value = currentValues.NODE_FONT;
    }

    function setupDialogHandlers(dialog) {
        if (handlersSetup) return;
        handlersSetup = true;

        addButtonHoverEffects(dialog);

        const elements = [
            'global-scale',
            'node-text-size',
            'node-subtext-size',
            'title-height',
            'slot-height',
            'group-font-size',
            'widget-text-size'
        ];

        elements.forEach(id => {
            const slider = dialog.querySelector(`#${id}`);
            const numberInput = dialog.querySelector(`#${id}-num`);
            if (slider && numberInput) {
                slider.oninput = () => {
                    numberInput.value = slider.value;
                    if (isPreviewMode) showPreviewIndicator();
                };
                numberInput.oninput = () => {
                    // Enforce min/max constraints
                    const min = parseFloat(numberInput.min);
                    const max = parseFloat(numberInput.max);
                    let value = parseFloat(numberInput.value);
                    if (value < min) value = min;
                    if (value > max) value = max;
                    numberInput.value = value;
                    slider.value = value;
                    if (isPreviewMode) showPreviewIndicator();
                };
            }
        });

        const saveBtn = dialog.querySelector('#save-defaults-btn');
        if (saveBtn) {
            saveBtn.onclick = () => {
                localStorage.setItem("endless_fontifier_defaults", JSON.stringify(currentValues));
                alert("🌊 Fontifier defaults saved! They'll auto-load next time.");
            };
        }

        dialog.querySelector('#apply-btn').onclick = () => {
            applyChanges(dialog, true);
            hidePreviewIndicator();
            closeDialog();
        };
        
        dialog.querySelector('#preview-btn').onclick = () => {
            applyChanges(dialog, false);
            showPreviewIndicator();
        };
        
        dialog.querySelector('#reset-btn').onclick = () => {
            localStorage.removeItem("endless_fontifier_defaults");
            currentValues = { ...originalValues };
            applySettingsToComfyUI(originalValues);
            updateDialogValues(dialog);
            hidePreviewIndicator();
            alert("🔁 Fontifier reset to ComfyUI defaults.");
        };
        
        dialog.querySelector('#cancel-btn').onclick = () => {
            applySettingsToComfyUI(dialogOpenValues);
            hidePreviewIndicator();
            closeDialog();
        };

        escHandler = e => {
            if (e.key === 'Escape') {
                applySettingsToComfyUI(dialogOpenValues);
                hidePreviewIndicator();
                closeDialog();
            }
        };
        document.addEventListener('keydown', escHandler);
    }

    function showPreviewIndicator() {
        if (!currentDialog) return;
        isPreviewMode = true;
        const indicator = currentDialog.querySelector('#preview-indicator');
        if (indicator) indicator.style.display = 'block';
    }

    function hidePreviewIndicator() {
        if (!currentDialog) return;
        isPreviewMode = false;
        const indicator = currentDialog.querySelector('#preview-indicator');
        if (indicator) indicator.style.display = 'none';
    }

    function applyChanges(dialog, permanent = false) {
        const globalScale = parseFloat(dialog.querySelector('#global-scale').value);
        
        const baseValues = {
            NODE_TEXT_SIZE: parseInt(dialog.querySelector('#node-text-size').value),
            NODE_SUBTEXT_SIZE: parseInt(dialog.querySelector('#node-subtext-size').value),
            NODE_TITLE_HEIGHT: parseInt(dialog.querySelector('#title-height').value),
            NODE_SLOT_HEIGHT: parseInt(dialog.querySelector('#slot-height').value),
            DEFAULT_GROUP_FONT: parseInt(dialog.querySelector('#group-font-size').value),
            FONT_FAMILY: dialog.querySelector('#font-family').value,
            NODE_FONT: dialog.querySelector('#font-family').value,
            WIDGET_TEXT_SIZE: parseInt(dialog.querySelector('#widget-text-size').value),
            GLOBAL_SCALE: globalScale
        };

        // Apply global scaling to font sizes
        const scaledValues = {
            ...baseValues,
            NODE_TEXT_SIZE: Math.round(baseValues.NODE_TEXT_SIZE * globalScale),
            NODE_SUBTEXT_SIZE: Math.round(baseValues.NODE_SUBTEXT_SIZE * globalScale),
            DEFAULT_GROUP_FONT: Math.round(baseValues.DEFAULT_GROUP_FONT * globalScale),
            WIDGET_TEXT_SIZE: Math.round(baseValues.WIDGET_TEXT_SIZE * globalScale)
        };

        applySettingsToComfyUI(scaledValues);
        if (permanent) {
            currentValues = { ...baseValues }; // Store unscaled values
            isPreviewMode = false;
        }
    }

    function applySettingsToComfyUI(settings) {
        LiteGraph.NODE_TEXT_SIZE = settings.NODE_TEXT_SIZE;
        LiteGraph.NODE_SUBTEXT_SIZE = settings.NODE_SUBTEXT_SIZE;
        LiteGraph.NODE_TITLE_HEIGHT = settings.NODE_TITLE_HEIGHT;
        LiteGraph.NODE_SLOT_HEIGHT = settings.NODE_SLOT_HEIGHT;
        LiteGraph.DEFAULT_GROUP_FONT = settings.DEFAULT_GROUP_FONT;
        LiteGraph.DEFAULT_GROUP_FONT_SIZE = settings.DEFAULT_GROUP_FONT;
        LiteGraph.NODE_FONT = settings.NODE_FONT;
        LiteGraph.DEFAULT_FONT = settings.NODE_FONT;
        LiteGraph.GROUP_FONT = settings.NODE_FONT;

        if (window.app?.canvas) {
            window.app.canvas.setDirty(true, true);
            setTimeout(() => window.app.canvas.draw(true, true), 100);
        }

        const styleId = "fontifier-widget-text-style";
        let styleTag = document.getElementById(styleId);
        if (!styleTag) {
            styleTag = document.createElement('style');
            styleTag.id = styleId;
            document.head.appendChild(styleTag);
        }
        styleTag.textContent = `
            .litegraph input, .litegraph select, .litegraph textarea {
                font-size: ${settings.WIDGET_TEXT_SIZE}px !important;
                font-family: ${settings.NODE_FONT} !important;
            }
            #fontifier-dialog input, #fontifier-dialog select, #fontifier-dialog textarea {
                font-size: 14px !important;
                font-family: Arial !important;
            }
        `;
    }

    function closeDialog() {
        if (currentDialog) currentDialog.remove();
        if (escHandler) document.removeEventListener('keydown', escHandler);
        if (unregisterThemeCallback) unregisterThemeCallback();
        // Clean up the style tag
        const styleTag = document.getElementById('fontifier-dialog-style');
        if (styleTag) styleTag.remove();
        currentDialog = null;
        handlersSetup = false;
        escHandler = null;
        unregisterThemeCallback = null;
        isPreviewMode = false;
    }

    // Wait for app to be ready before initializing
    function waitForApp() {
        if (typeof window.app !== 'undefined' && window.app?.canvas) {
            // Initialize with saved defaults once app is ready
            applySettingsToComfyUI(currentValues);
            return;
        }
        setTimeout(waitForApp, 100);
    }
    
    waitForApp();

    // Register into Endless Tools menu
    registerEndlessTool("Fontifier", createFontifierDialog);
})();