// ComfyUI Endless 🌊✨ Fontifier - Improved Version

(function() {
    'use strict';
    
    // Store original values for reset functionality
    const originalValues = {
        NODE_TEXT_SIZE: 14,
        NODE_SUBTEXT_SIZE: 12,
        NODE_TITLE_HEIGHT: 30,
        DEFAULT_GROUP_FONT: 24,
        NODE_FONT: 'Arial',
        NODE_SLOT_HEIGHT: 20,
        NODE_WIDGET_HEIGHT: 20
    };
    
    // Current values (will be updated as user changes them)
    let currentValues = { ...originalValues };
    
    // Get ComfyUI theme colors
    function getComfyUIColors() {
        const computedStyle = getComputedStyle(document.documentElement);
        return {
            background: computedStyle.getPropertyValue('--comfy-menu-bg') || '#353535',
            backgroundSecondary: computedStyle.getPropertyValue('--comfy-input-bg') || '#222',
            border: computedStyle.getPropertyValue('--border-color') || '#999',
            text: computedStyle.getPropertyValue('--input-text') || '#ddd',
            textSecondary: computedStyle.getPropertyValue('--descrip-text') || '#999',
            accent: computedStyle.getPropertyValue('--comfy-menu-bg') || '#0f0f0f'
        };
    }

    function makeDraggable(dialog) {
        const header = dialog.querySelector('h2');
        if (!header) return;

        let offsetX = 0, offsetY = 0, isDown = false;

        header.style.cursor = 'move';
        header.style.userSelect = 'none';
        
        header.onmousedown = (e) => {
            e.preventDefault();
            isDown = true;
            
            // Get the actual position of the dialog
            const rect = dialog.getBoundingClientRect();
            offsetX = e.clientX - rect.left;
            offsetY = e.clientY - rect.top;
            
            const onMouseMove = (e) => {
                if (!isDown) return;
                e.preventDefault();
                dialog.style.left = `${e.clientX - offsetX}px`;
                dialog.style.top = `${e.clientY - offsetY}px`;
                dialog.style.transform = 'none'; // Remove the centering transform
            };
            
            const onMouseUp = () => {
                isDown = false;
                document.removeEventListener('mousemove', onMouseMove);
                document.removeEventListener('mouseup', onMouseUp);
            };
            
            document.addEventListener('mousemove', onMouseMove);
            document.addEventListener('mouseup', onMouseUp);
        };
    }
        
    function createFontifierDialog() {
        // Remove existing dialog if present
        const existingDialog = document.getElementById('fontifier-dialog');
        if (existingDialog) {
            existingDialog.remove();
        }
        
        const colors = getComfyUIColors();
        
        // Create dialog container
        const dialog = document.createElement('div');
        dialog.id = 'fontifier-dialog';
        dialog.className = 'comfyui-dialog';
        dialog.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: ${colors.background};
            border: 1px solid ${colors.border};
            border-radius: 8px;
            padding: 20px;
            z-index: 10000;
            width: 520px;
            max-height: 80vh;
            overflow-y: auto;
            font-family: Arial, sans-serif;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            color: ${colors.text};
        `;
        
        // Create backdrop
        const backdrop = document.createElement('div');
        backdrop.className = 'comfyui-backdrop';
        backdrop.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            z-index: 9999;
        `;
        backdrop.onclick = () => {
            backdrop.remove();
            dialog.remove();
        };
        
        dialog.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; border-bottom: 1px solid ${colors.border}; padding-bottom: 15px;">
                <h2 style="color: ${colors.text}; margin: 0; font-size: 16px;">🌊✨ Endless Fontifier</h2>
                <button id="close-dialog" style="background: ${colors.backgroundSecondary}; border: 1px solid ${colors.border}; color: ${colors.text}; padding: 6px 12px; border-radius: 4px; cursor: pointer;">✕</button>
            </div>
            
            <div style="margin-bottom: 12px; padding: 12px; background: ${colors.backgroundSecondary}; border-radius: 6px; border: 1px solid ${colors.border};">
                <h3 style="color: ${colors.text}; margin: 0 0 10px 0; font-size: 16px;">Global Scale</h3>
                <div style="display: flex; align-items: center; gap: 12px;">
                    <label style="color: ${colors.textSecondary}; min-width: 80px; font-size: 12px;">Scale All:</label>
                    <input type="range" id="global-scale" min="0.5" max="3" step="0.1" value="1" style="flex: 1; accent-color: ${colors.accent};">
                    <input type="number" id="global-scale-num" min="0.5" max="3" step="0.1" value="1" style="width: 70px; padding: 6px; background: ${colors.background}; border: 1px solid ${colors.border}; color: ${colors.text}; border-radius: 4px; font-size: 12px;">
                </div>
            </div>
            
            <div style="margin-bottom: 12px; padding: 12px; background: ${colors.backgroundSecondary}; border-radius: 6px; border: 1px solid ${colors.border};">
                <h3 style="color: ${colors.text}; margin: 0 0 12px 0; font-size: 16px;">Font Family</h3>
                <select id="font-family" style="width: 100%; padding: 8px; background: ${colors.background}; border: 1px solid ${colors.border}; color: ${colors.text}; border-radius: 4px; font-size: 12px;">
                    <option value="Arial">Arial</option>
                    <option value="Helvetica">Helvetica</option>
                    <option value="Times New Roman">Times New Roman</option>
                    <option value="Courier New">Courier New</option>
                    <option value="Verdana">Verdana</option>
                    <option value="Georgia">Georgia</option>
                    <option value="Comic Sans MS">Comic Sans MS</option>
                    <option value="Impact">Impact</option>
                    <option value="Trebuchet MS">Trebuchet MS</option>
                    <option value="Tahoma">Tahoma</option>
                </select>
            </div>
            
            <div style="margin-bottom: 12px; padding: 12px; background: ${colors.backgroundSecondary}; border-radius: 6px; border: 1px solid ${colors.border};">
                <h3 style="color: ${colors.text}; margin: 0 0 12px 0; font-size: 16px;">Text Element Sizes</h3>
                
                <div style="margin-bottom: 10px;">
                    <label style="color: ${colors.text}; display: block; margin-bottom: 4px; font-size: 12px; font-weight: bold;">Node Title Text</label>
                    <div style="color: ${colors.textSecondary}; font-size: 10px; margin-bottom: 5px;">The main title text at the top of each node (e.g., "KSampler", "VAE Decode")</div>
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <input type="range" id="node-text-size" min="8" max="32" value="${currentValues.NODE_TEXT_SIZE}" style="flex: 1; accent-color: ${colors.accent};">
                        <input type="number" id="node-text-size-num" min="8" max="32" value="${currentValues.NODE_TEXT_SIZE}" style="width: 60px; padding: 5px; background: ${colors.background}; border: 1px solid ${colors.border}; color: ${colors.text}; border-radius: 4px; font-size: 12px;">
                    </div>
                </div>
                
                <div style="margin-bottom: 10px;">
                    <label style="color: ${colors.text}; display: block; margin-bottom: 4px; font-size: 12px; font-weight: bold;">Widget Labels & Values</label>
                    <div style="color: ${colors.textSecondary}; font-size: 10px; margin-bottom: 5px;">Text inside nodes: parameter names and values (e.g., "steps: 20", "cfg: 8.0")</div>
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <input type="range" id="node-subtext-size" min="6" max="24" value="${currentValues.NODE_SUBTEXT_SIZE}" style="flex: 1; accent-color: ${colors.accent};">
                        <input type="number" id="node-subtext-size-num" min="6" max="24" value="${currentValues.NODE_SUBTEXT_SIZE}" style="width: 60px; padding: 5px; background: ${colors.background}; border: 1px solid ${colors.border}; color: ${colors.text}; border-radius: 4px; font-size: 12px;">
                    </div>
                </div>
                <div style="margin-bottom: 10px;">
                    <label style="color: ${colors.text}; display: block; margin-bottom: 4px; font-size: 12px; font-weight: bold;">Widget Text Input Size</label>
                    <div style="color: ${colors.textSecondary}; font-size: 10px; margin-bottom: 5px;">Font size for text inside input boxes, dropdowns, and textareas in nodes.</div>
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <input type="range" id="widget-text-size" min="8" max="24" value="12" style="flex: 1; accent-color: ${colors.accent};">
                        <input type="number" id="widget-text-size-num" min="8" max="24" value="12" style="width: 60px; padding: 5px; background: ${colors.background}; border: 1px solid ${colors.border}; color: ${colors.text}; border-radius: 4px; font-size: 12px;">
                    </div>
                </div>


                <div style="margin-bottom: 10px;">
                    <label style="color: ${colors.text}; display: block; margin-bottom: 4px; font-size: 12px; font-weight: bold;">Node Title Area Height</label>
                    <div style="color: ${colors.textSecondary}; font-size: 10px; margin-bottom: 5px;">Height of the colored title bar area at the top of nodes</div>
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <input type="range" id="title-height" min="20" max="60" value="${currentValues.NODE_TITLE_HEIGHT}" style="flex: 1; accent-color: ${colors.accent};">
                        <input type="number" id="title-height-num" min="20" max="60" value="${currentValues.NODE_TITLE_HEIGHT}" style="width: 60px; padding: 5px; background: ${colors.background}; border: 1px solid ${colors.border}; color: ${colors.text}; border-radius: 4px; font-size: 12px;">
                    </div>
                </div>
                
                <div style="margin-bottom: 10px;">
                    <label style="color: ${colors.text}; display: block; margin-bottom: 4px; font-size: 12px; font-weight: bold;">Connection Slot Height</label>
                    <div style="color: ${colors.textSecondary}; font-size: 10px; margin-bottom: 5px;">Height of input/output connection points on node sides</div>
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <input type="range" id="slot-height" min="12" max="40" value="${currentValues.NODE_SLOT_HEIGHT}" style="flex: 1; accent-color: ${colors.accent};">
                        <input type="number" id="slot-height-num" min="12" max="40" value="${currentValues.NODE_SLOT_HEIGHT}" style="width: 60px; padding: 5px; background: ${colors.background}; border: 1px solid ${colors.border}; color: ${colors.text}; border-radius: 4px; font-size: 12px;">
                    </div>
                </div>
                
                <div style="margin-bottom: 10px;">
                    <label style="color: ${colors.text}; display: block; margin-bottom: 4px; font-size: 12px; font-weight: bold;">Group Label Size</label>
                    <div style="color: ${colors.textSecondary}; font-size: 10px; margin-bottom: 5px;">Text size for node group labels (when nodes are grouped together)</div>
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <input type="range" id="group-font-size" min="12" max="48" value="${currentValues.DEFAULT_GROUP_FONT}" style="flex: 1; accent-color: ${colors.accent};">
                        <input type="number" id="group-font-size-num" min="12" max="48" value="${currentValues.DEFAULT_GROUP_FONT}" style="width: 60px; padding: 5px; background: ${colors.background}; border: 1px solid ${colors.border}; color: ${colors.text}; border-radius: 4px; font-size: 12px;">
                    </div>
                </div>
            </div>
            
            <div style="display: flex; gap: 10px; justify-content: center; padding-top: 15px; border-top: 1px solid ${colors.border};">
                <button id="reset-btn" style="padding: 8px 16px; background: ${colors.backgroundSecondary}; border: 1px solid ${colors.border}; color: ${colors.text}; border-radius: 4px; cursor: pointer; font-size: 12px; transition: border-width 0.2s ease;">Reset</button>
                <button id="preview-btn" style="padding: 8px 16px; background: ${colors.backgroundSecondary}; border: 1px solid ${colors.border}; color: ${colors.text}; border-radius: 4px; cursor: pointer; font-size: 12px; transition: border-width 0.2s ease;">Preview</button>
                <button id="apply-btn" style="padding: 8px 16px; background: ${colors.backgroundSecondary}; border: 1px solid ${colors.border}; color: ${colors.text}; border-radius: 4px; cursor: pointer; font-size: 12px; transition: border-width 0.2s ease; background-image: linear-gradient(rgba(128, 255, 128, 0.08), rgba(128, 255, 128, 0.08));">Apply & Close</button>
                <button id="cancel-btn" style="padding: 8px 16px; background: ${colors.backgroundSecondary}; border: 1px solid ${colors.border}; color: ${colors.textSecondary}; border-radius: 4px; cursor: pointer; font-size: 12px; transition: border-width 0.2s ease; background-image: linear-gradient(rgba(255, 128, 128, 0.08), rgba(255, 128, 128, 0.08));">Cancel</button>
            </div>
        `;
        
            document.body.appendChild(backdrop);
            document.body.appendChild(dialog);

            // ESC key handler
            document.addEventListener('keydown', function escHandler(e) {
                if (e.key === 'Escape') {
                    backdrop.remove();
                    dialog.remove();
                    document.removeEventListener('keydown', escHandler);
                }
            });

            // Set up event handlers
            setupDialogHandlers(dialog, backdrop);
    }
    
    function setupDialogHandlers(dialog, backdrop) {

// call drag function

    makeDraggable(dialog);

        // Sync sliders with number inputs
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
            
            slider.oninput = () => {
                numberInput.value = slider.value;
                // Update global scale number input properly
                if (id === 'global-scale') {
                    const globalScaleNum = dialog.querySelector('#global-scale-num');
                    globalScaleNum.value = slider.value;
                }
            };
            numberInput.oninput = () => {
                slider.value = numberInput.value;
            };
        });
        
        // Global scale handler
        const globalScale = dialog.querySelector('#global-scale');
        const globalScaleNum = dialog.querySelector('#global-scale-num');
        
        function updateGlobalScale() {
            const scale = parseFloat(globalScale.value);
            globalScaleNum.value = scale; // Fix: Update the number input
            
            // Update all individual controls
            const updates = [
                ['node-text-size', originalValues.NODE_TEXT_SIZE],
                ['node-subtext-size', originalValues.NODE_SUBTEXT_SIZE],
                ['title-height', originalValues.NODE_TITLE_HEIGHT],
                ['slot-height', originalValues.NODE_SLOT_HEIGHT],
                ['group-font-size', originalValues.DEFAULT_GROUP_FONT]
            ];
            
            updates.forEach(([id, originalValue]) => {
                const newValue = Math.round(originalValue * scale);
                dialog.querySelector(`#${id}`).value = newValue;
                dialog.querySelector(`#${id}-num`).value = newValue;
            });
        }
        
        globalScale.oninput = updateGlobalScale;
        globalScaleNum.oninput = () => {
            globalScale.value = globalScaleNum.value;
            updateGlobalScale();
        };
        
        // Button handlers
        dialog.querySelector('#close-dialog').onclick = () => {
            backdrop.remove();
            dialog.remove();
        };
        
        dialog.querySelector('#reset-btn').onclick = () => {
            dialog.querySelector('#global-scale').value = 1;
            dialog.querySelector('#global-scale-num').value = 1;
            dialog.querySelector('#node-text-size').value = originalValues.NODE_TEXT_SIZE;
            dialog.querySelector('#node-text-size-num').value = originalValues.NODE_TEXT_SIZE;
            dialog.querySelector('#node-subtext-size').value = originalValues.NODE_SUBTEXT_SIZE;
            dialog.querySelector('#node-subtext-size-num').value = originalValues.NODE_SUBTEXT_SIZE;
            dialog.querySelector('#title-height').value = originalValues.NODE_TITLE_HEIGHT;
            dialog.querySelector('#title-height-num').value = originalValues.NODE_TITLE_HEIGHT;
            dialog.querySelector('#slot-height').value = originalValues.NODE_SLOT_HEIGHT;
            dialog.querySelector('#slot-height-num').value = originalValues.NODE_SLOT_HEIGHT;
            dialog.querySelector('#group-font-size').value = originalValues.DEFAULT_GROUP_FONT;
            dialog.querySelector('#group-font-size-num').value = originalValues.DEFAULT_GROUP_FONT;
            dialog.querySelector('#font-family').value = 'Arial';
        };
        
        dialog.querySelector('#preview-btn').onclick = () => applyChanges(dialog, false);
        
        dialog.querySelector('#apply-btn').onclick = () => {
            applyChanges(dialog, true);
            backdrop.remove();
            dialog.remove();
        };
        
        dialog.querySelector('#cancel-btn').onclick = () => {
            backdrop.remove();
            dialog.remove();
        };

        // Add hover effects to buttons
        const buttons = dialog.querySelectorAll('button');
        buttons.forEach(button => {
            button.style.boxSizing = 'border-box';
            button.style.minWidth = button.offsetWidth + 'px'; // Lock the width
            button.addEventListener('mouseenter', () => {
                button.style.borderWidth = '2px';
                button.style.padding = '7px 15px';
            });
            button.addEventListener('mouseleave', () => {
                button.style.borderWidth = '1px';
                button.style.padding = '8px 16px';
            });
        });
    }
    
    function applyChanges(dialog, permanent = false) {
        const newValues = {
            NODE_TEXT_SIZE: parseInt(dialog.querySelector('#node-text-size').value),
            NODE_SUBTEXT_SIZE: parseInt(dialog.querySelector('#node-subtext-size').value),
            NODE_TITLE_HEIGHT: parseInt(dialog.querySelector('#title-height').value),
            NODE_SLOT_HEIGHT: parseInt(dialog.querySelector('#slot-height').value),
            DEFAULT_GROUP_FONT: parseInt(dialog.querySelector('#group-font-size').value),
            FONT_FAMILY: dialog.querySelector('#font-family').value
        };

        if (typeof LiteGraph !== 'undefined') {
            LiteGraph.NODE_TEXT_SIZE = newValues.NODE_TEXT_SIZE;
            LiteGraph.NODE_SUBTEXT_SIZE = newValues.NODE_SUBTEXT_SIZE;
            LiteGraph.NODE_TITLE_HEIGHT = newValues.NODE_TITLE_HEIGHT;
            LiteGraph.NODE_SLOT_HEIGHT = newValues.NODE_SLOT_HEIGHT;
            LiteGraph.NODE_WIDGET_HEIGHT = newValues.NODE_SLOT_HEIGHT;
            LiteGraph.DEFAULT_GROUP_FONT = newValues.DEFAULT_GROUP_FONT;
            LiteGraph.DEFAULT_GROUP_FONT_SIZE = newValues.DEFAULT_GROUP_FONT;
            LiteGraph.NODE_FONT = newValues.FONT_FAMILY;
            LiteGraph.DEFAULT_FONT = newValues.FONT_FAMILY;
            LiteGraph.GROUP_FONT = newValues.FONT_FAMILY;

            console.log('🌊✨ Fontifier applied:', newValues);

            if (typeof app !== 'undefined' && app.canvas) {
                app.canvas.setDirty(true, true);
                if (app.canvas.draw) {
                    setTimeout(() => app.canvas.draw(true, true), 100);
                }
            }

            const canvases = document.querySelectorAll('canvas');
            canvases.forEach(canvas => {
                if (canvas.getContext) {
                    const ctx = canvas.getContext('2d');
                    const originalWidth = canvas.width;
                    canvas.width = originalWidth + 1;
                    canvas.width = originalWidth;
                }
            });
        }

        // Apply widget font size to CSS, this is DOM-only
        const widgetTextSize = parseInt(dialog.querySelector('#widget-text-size').value);
        let styleTag = document.getElementById('fontifier-widget-text-style');
        if (!styleTag) {
            styleTag = document.createElement('style');
            styleTag.id = 'fontifier-widget-text-style';
            document.head.appendChild(styleTag);
        }
        styleTag.textContent = `
            canvas ~ * .widget input, canvas ~ * .widget select, canvas ~ * .widget textarea,
            canvas ~ * .comfy-multiline-input, canvas ~ * .comfy-input, 
            canvas ~ * input.comfy-multiline-input, canvas ~ * textarea.comfy-multiline-input,
            canvas ~ * [class*="comfy-input"], canvas ~ * [class*="comfy-multiline"],
            canvas ~ * .comfyui-widget input, canvas ~ * .comfyui-widget select, canvas ~ * .comfyui-widget textarea,
            canvas ~ * [class*="widget"] input, canvas ~ * [class*="widget"] select, canvas ~ * [class*="widget"] textarea,
            canvas ~ * .litegraph input, canvas ~ * .litegraph select, canvas ~ * .litegraph textarea,
            .litegraph input, .litegraph select, .litegraph textarea {
                font-size: ${widgetTextSize}px !important;
                font-family: ${newValues.FONT_FAMILY} !important;
            }
            
            /* Exclude the fontifier dialog itself */
            #fontifier-dialog input, #fontifier-dialog select, #fontifier-dialog textarea {
                font-size: 14px !important;
                font-family: Arial !important;
            }
        `;

        if (permanent) {
            currentValues = { ...newValues };
            console.log('🌊✨ Fontifier changes applied permanently (until page refresh)');
        }
    }

    
    function findToolbar() {
        // Method 1: Look for ComfyUI specific toolbar classes
        let toolbar = document.querySelector('.comfyui-menu, .comfy-menu, [class*="menu"], [class*="toolbar"]');
        
        // Method 2: Look for button groups
        if (!toolbar) {
            const buttonGroups = document.querySelectorAll('[class*="button-group"], [class*="btn-group"], .comfyui-button-group');
            toolbar = Array.from(buttonGroups).find(group => 
                group.querySelectorAll('button').length > 0
            );
        }
        
        // Method 3: Look for any container with multiple buttons
        if (!toolbar) {
            const allElements = document.querySelectorAll('*');
            toolbar = Array.from(allElements).find(el => {
                const buttons = el.querySelectorAll('button');
                return buttons.length >= 2 && buttons.length <= 10; // Reasonable toolbar size
            });
        }
        
        // Method 4: Fallback to the original Share button method
        if (!toolbar) {
            toolbar = Array.from(document.querySelectorAll(".comfyui-button-group")).find(div =>
                Array.from(div.querySelectorAll("button")).some(btn => btn.title === "Share")
            );
        }
        
        return toolbar;
    }
    
    function injectFontifierButton() {
        const toolbar = findToolbar();
        
        if (toolbar && !document.getElementById("endless-fontifier-button")) {
            const colors = getComfyUIColors();
            
            const btn = document.createElement("button");
            btn.id = "endless-fontifier-button";
            btn.textContent = "🌊✨ Fontifier";
            btn.className = "comfyui-button";

            // Function to update button colors
            function updateButtonColors() {
                const currentColors = getComfyUIColors();
                btn.style.cssText = `
                    margin-left: 8px;
                    background: ${currentColors.backgroundSecondary};
                    border: 1px solid ${currentColors.border};
                    color: ${currentColors.text};
                    padding: 6px 12px;
                    border-radius: 4px;
                    cursor: pointer;
                    font-size: 14px;
                    transition: all 0.2s ease;
                `;
                
                btn.onmouseover = () => {
                    const hoverColors = getComfyUIColors();
                    btn.style.background = hoverColors.background;
                    btn.style.borderColor = hoverColors.text;
                };
                
                btn.onmouseout = () => {
                    const outColors = getComfyUIColors();
                    btn.style.background = outColors.backgroundSecondary;
                    btn.style.borderColor = outColors.border;
                };
            }

            // Initial colors
            updateButtonColors();

            // Watch for theme changes
            const observer = new MutationObserver(updateButtonColors);
            observer.observe(document.documentElement, { 
                attributes: true, 
                attributeFilter: ['class', 'style'] 
            });

            btn.onclick = createFontifierDialog;
            toolbar.appendChild(btn);
            
            console.log("✅ 🌊✨ Endless Fontifier button injected successfully!");
            return true;
        }
        return false;
    }
    
    // Try to inject immediately
    if (!injectFontifierButton()) {
        // If immediate injection fails, use observer
        const observer = new MutationObserver(() => {
            if (injectFontifierButton()) {
                observer.disconnect();
            }
        });
        
        observer.observe(document.body, { childList: true, subtree: true });
        
        // Timeout after 30 seconds to avoid infinite observation
        setTimeout(() => {
            observer.disconnect();
            if (!document.getElementById("endless-fontifier-button")) {
                console.warn("⚠️ Could not find suitable toolbar for Fontifier button");
            }
        }, 30000);
    }
})();