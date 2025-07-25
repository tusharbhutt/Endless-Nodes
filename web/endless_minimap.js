// ComfyUI Endless 🌊✨ Minimap - Optimized Version

(function waitForHelpers() {
    if (typeof window.EndlessHelpers === 'undefined') {
        console.warn("⏳ Waiting for EndlessHelpers to be ready...");
        setTimeout(waitForHelpers, 100);
        return;
    }

    const {
        registerEndlessTool,
        onThemeChange,
        getComfyUIColors,
        toRGBA,
        makeDraggable
    } = window.EndlessHelpers;

    console.log("✅ Endless Minimap loaded.");

    // State variables
    let currentDialog = null;
    let animationId = null;
    let unregisterThemeCallback = null;
    let resizeObserver = null;

    // Canvas state
    let panX = 0, panY = 0, zoom = 1;
    let isDragging = false;
    let dragStartTime = 0, dragStartX = 0, dragStartY = 0;
    const DRAG_THRESHOLD = 5;

    // Size constants
    const BASE_WIDTH = 300, BASE_HEIGHT = 400;
    const MAX_WIDTH = 500, MAX_HEIGHT = 600;
    const MIN_WIDTH = 200, MIN_HEIGHT = 150;

    // Node type colors - comprehensive mapping
    const NODE_COLORS = {
        // Image Processing (Blue family)
        'LoadImage': '#5DADE2', 'SaveImage': '#3498DB', 'PreviewImage': '#2E86AB',
        'ImageScale': '#85C1E9', 'ImageCrop': '#7FB3D3', 'ImageBlend': '#6BB6FF',
        
        // Latent Processing (Purple family)
        'KSampler': '#8E44AD', 'KSamplerAdvanced': '#9B59B6', 'EmptyLatentImage': '#A569BD',
        'LatentUpscale': '#BB8FCE', 'LatentBlend': '#D2B4DE',
        
        // VAE (Green family)
        'VAEDecode': '#27AE60', 'VAEEncode': '#2ECC71', 'VAELoader': '#58D68D',
        
        // Model/Checkpoint (Teal family)
        'CheckpointLoaderSimple': '#17A2B8', 'CheckpointLoader': '#148A99',
        'ModelMergeSimple': '#1ABC9C', 'UNETLoader': '#5DADE2',
        
        // CLIP/Text (Orange family)
        'CLIPTextEncode': '#E67E22', 'CLIPTextEncodeSDXL': '#F39C12',
        'CLIPLoader': '#F8C471', 'CLIPVisionEncode': '#D68910',
        
        // LoRA (Yellow family)
        'LoraLoader': '#F1C40F', 'LoraLoaderModelOnly': '#F4D03F',
        
        // ControlNet (Pink family)
        'ControlNetLoader': '#E91E63', 'ControlNetApply': '#F06292',
        'CannyEdgePreprocessor': '#EC407A', 'OpenposePreprocessor': '#F8BBD9',
        
        // Conditioning (Coral family)
        'ConditioningAverage': '#FF6B35', 'ConditioningCombine': '#FF8C42',
        
        // Utility (Gray family)
        'PrimitiveNode': '#95A5A6', 'Note': '#BDC3C7', 'Reroute': '#85929E',
        
        // Upscaling (Lime family)
        'UpscaleModelLoader': '#7FB069', 'ImageUpscaleWithModel': '#8BC34A',
        
        // Masks (Red family)
        'MaskComposite': '#E53935', 'MaskToImage': '#F44336', 'ImageToMask': '#EF5350',
        
        'default': 'rgba(200, 200, 200, 0.7)'
    };

    function getApp() {
        return window.app || window.comfyApp || document.querySelector('#app')?.__vue__?.$root || null;
    }

    function getCanvasAspectRatio() {
        const mainCanvas = document.querySelector('canvas') || 
                          document.querySelector('#graph-canvas') ||
                          document.querySelector('.litegraph');
        
        if (mainCanvas) {
            const rect = mainCanvas.getBoundingClientRect();
            return rect.width / rect.height;
        }
        
        return window.innerWidth / window.innerHeight;
    }

    function calculateDimensions() {
        const aspectRatio = getCanvasAspectRatio();
        let containerWidth, containerHeight, canvasWidth, canvasHeight;
        
        if (aspectRatio > 1) {
            containerWidth = Math.max(MIN_WIDTH, Math.min(MAX_WIDTH, BASE_WIDTH * aspectRatio));
            containerHeight = BASE_HEIGHT;
            canvasWidth = containerWidth;
            canvasHeight = BASE_HEIGHT - 50;
        } else {
            containerWidth = BASE_WIDTH;
            containerHeight = Math.max(MIN_HEIGHT, Math.min(MAX_HEIGHT, BASE_HEIGHT / aspectRatio));
            canvasWidth = containerWidth;
            canvasHeight = containerHeight - 50;
        }
        
        return { containerWidth, containerHeight, canvasWidth, canvasHeight };
    }

    function getNodeColor(node) {
        const nodeType = node.type || node.constructor?.name || 'default';
        
        if (NODE_COLORS[nodeType]) return NODE_COLORS[nodeType];
        
        // Pattern matching for common types
        const patterns = [
            ['Sampler', NODE_COLORS['KSampler']],
            ['CLIP', NODE_COLORS['CLIPTextEncode']],
            ['VAE', NODE_COLORS['VAEDecode']],
            ['ControlNet', NODE_COLORS['ControlNetLoader']],
            ['Lora', NODE_COLORS['LoraLoader']],
            ['Image.*Load', NODE_COLORS['LoadImage']],
            ['Image.*Save', NODE_COLORS['SaveImage']],
            ['Checkpoint', NODE_COLORS['CheckpointLoaderSimple']],
            ['Upscale', NODE_COLORS['UpscaleModelLoader']],
            ['Mask', NODE_COLORS['MaskComposite']]
        ];
        
        for (const [pattern, color] of patterns) {
            if (new RegExp(pattern, 'i').test(nodeType)) return color;
        }
        
        return NODE_COLORS.default;
    }

    function getNodes() {
        const app = getApp();
        if (!app) {
            console.log("App not found, trying DOM fallback...");
            const nodeElements = document.querySelectorAll('[class*="node"], .comfy-node, .litegraph-node');
            if (nodeElements.length > 0) {
                return Array.from(nodeElements).map((el, i) => ({
                    pos: [i * 150, i * 100],
                    size: [100, 60],
                    type: 'Unknown',
                    title: `Node ${i + 1}`
                }));
            }
            return null;
        }

        const nodes = app.graph?._nodes || 
                     app.graph?.nodes || 
                     app.canvas?.graph?._nodes ||
                     app.canvas?.graph?.nodes ||
                     [];
        
        return nodes;
    }

    function createStyleCSS(colors) {
        return `
            #endless-minimap button {
                background: none;
                border: none;
                color: ${colors.inputText};
                cursor: pointer;
                padding: 2px 6px;
                font-size: 18px;
                border-radius: 3px;
                transition: background 0.2s ease;
            }
            #endless-minimap button:hover {
                background: ${toRGBA(colors.inputText, 0.1)};
            }
            #endless-minimap .drag-bar {
                padding: 4px 8px;
                background: ${toRGBA(colors.inputText, 0.05)};
                cursor: move;
                font-size: 14px;
                user-select: none;
                border-bottom: 1px solid ${colors.border};
                flex-shrink: 0;
            }
            #endless-minimap .legend {
                position: absolute;
                top: 5px;
                left: 5px;
                background: ${colors.menu};
                color: ${colors.inputText};
                padding: 8px;
                border: 1px solid ${colors.border};
                border-radius: 4px;
                font-size: 10px;
                max-height: 200px;
                overflow-y: auto;
                display: none;
                z-index: 1;
            }
            #endless-minimap .pan-info {
                padding: 2px 8px;
                font-size: 10px;
                background: ${colors.menuSecondary};
                color: ${colors.inputText};
                border-top: 1px solid ${colors.border};
                text-align: center;
                flex-shrink: 0;
            }
        `;
    }

    function updateTheme() {
        if (!currentDialog) return;
        
        const colors = getComfyUIColors();
        
        // Update container colors only, not size
        currentDialog.style.background = colors.menu;
        currentDialog.style.color = colors.inputText;
        currentDialog.style.borderColor = colors.accent;
        
        // Update style tag
        const styleTag = document.getElementById('minimap-style');
        if (styleTag) {
            styleTag.textContent = createStyleCSS(colors);
        }
        
        drawMinimap();
    }

    function updateLegend() {
        const legend = currentDialog.querySelector('.legend');
        if (!legend || legend.style.display === 'none') return;
        
        const nodes = getNodes();
        if (!nodes) return;

        const typeCounts = {};
        nodes.forEach(n => {
            const nodeType = n.type || n.constructor?.name || 'default';
            typeCounts[nodeType] = (typeCounts[nodeType] || 0) + 1;
        });

        legend.innerHTML = Object.entries(typeCounts)
            .sort((a, b) => b[1] - a[1])
            .map(([type, count]) => {
                const color = NODE_COLORS[type] || NODE_COLORS.default;
                return `<div style="margin: 2px 0; display: flex; align-items: center;">
                    <div style="width: 12px; height: 12px; background: ${color}; margin-right: 6px; border-radius: 2px;"></div>
                    <span>${type} (${count})</span>
                </div>`;
            }).join('');
    }

    // Get current transform state for coordinate conversions
    function getTransformState() {
        const canvas = currentDialog?.querySelector('canvas');
        if (!canvas) return null;

        const nodes = getNodes();
        if (!nodes?.length) return null;

        // Calculate bounds (same as in drawMinimap)
        const bounds = nodes.reduce((acc, n) => {
            const x = n.pos?.[0] ?? n.x ?? 0;
            const y = n.pos?.[1] ?? n.y ?? 0;
            const w = n.size?.[0] ?? n.width ?? 100;
            const h = n.size?.[1] ?? n.height ?? 60;
            
            return {
                minX: Math.min(acc.minX, x),
                minY: Math.min(acc.minY, y),
                maxX: Math.max(acc.maxX, x + w),
                maxY: Math.max(acc.maxY, y + h)
            };
        }, { minX: Infinity, minY: Infinity, maxX: -Infinity, maxY: -Infinity });

        const width = bounds.maxX - bounds.minX;
        const height = bounds.maxY - bounds.minY;
        if (width <= 0 || height <= 0) return null;

        const baseScale = Math.min(canvas.width / Math.max(width, 1000), canvas.height / Math.max(height, 1000));
        const scale = baseScale * zoom;

        return {
            bounds,
            width,
            height,
            scale,
            canvas
        };
    }

    // Convert canvas coordinates to world coordinates
    function canvasToWorld(canvasX, canvasY) {
        const transform = getTransformState();
        if (!transform) return null;

        const { bounds, width, height, scale, canvas } = transform;

        // Inverse of the transform used in drawMinimap
        const worldX = (canvasX - canvas.width / 2 - panX) / scale + (bounds.minX + width / 2);
        const worldY = (canvasY - canvas.height / 2 - panY) / scale + (bounds.minY + height / 2);

        return { x: worldX, y: worldY };
    }

    // Convert world coordinates to canvas coordinates
    function worldToCanvas(worldX, worldY) {
        const transform = getTransformState();
        if (!transform) return null;

        const { bounds, width, height, scale, canvas } = transform;

        // Same transform as used in drawMinimap
        const canvasX = (worldX - (bounds.minX + width / 2)) * scale + canvas.width / 2 + panX;
        const canvasY = (worldY - (bounds.minY + height / 2)) * scale + canvas.height / 2 + panY;

        return { x: canvasX, y: canvasY };
    }

    function drawMinimap() {
        if (!currentDialog) return;
        
        const canvas = currentDialog.querySelector('canvas');
        const panInfo = currentDialog.querySelector('.pan-info');
        if (!canvas || !panInfo) return;
        
        const ctx = canvas.getContext('2d');
        const colors = getComfyUIColors();
        
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        const nodes = getNodes();
        if (!nodes || !nodes.length) {
            ctx.fillStyle = colors.inputText;
            ctx.font = '12px Arial';
            ctx.textAlign = 'center';
            ctx.fillText('No nodes found', canvas.width / 2, canvas.height / 2);
            ctx.fillText('or graph not loaded', canvas.width / 2, canvas.height / 2 + 15);
            return;
        }

        // Calculate bounds
        const bounds = nodes.reduce((acc, n) => {
            const x = n.pos?.[0] ?? n.x ?? 0;
            const y = n.pos?.[1] ?? n.y ?? 0;
            const w = n.size?.[0] ?? n.width ?? 100;
            const h = n.size?.[1] ?? n.height ?? 60;
            
            return {
                minX: Math.min(acc.minX, x),
                minY: Math.min(acc.minY, y),
                maxX: Math.max(acc.maxX, x + w),
                maxY: Math.max(acc.maxY, y + h)
            };
        }, { minX: Infinity, minY: Infinity, maxX: -Infinity, maxY: -Infinity });

        const width = bounds.maxX - bounds.minX;
        const height = bounds.maxY - bounds.minY;
        if (width <= 0 || height <= 0) return;

        const baseScale = Math.min(canvas.width / Math.max(width, 1000), canvas.height / Math.max(height, 1000));
        const scale = baseScale * zoom;

        ctx.save();
        ctx.translate(canvas.width / 2 + panX, canvas.height / 2 + panY);
        ctx.scale(scale, scale);
        ctx.translate(-(bounds.minX + width/2), -(bounds.minY + height/2));

        // Draw grid
        ctx.strokeStyle = toRGBA(colors.inputText, 0.1);
        ctx.lineWidth = 1 / scale;
        const gridSize = 100;
        for (let x = Math.floor(bounds.minX / gridSize) * gridSize; x <= bounds.maxX; x += gridSize) {
            ctx.beginPath();
            ctx.moveTo(x, bounds.minY);
            ctx.lineTo(x, bounds.maxY);
            ctx.stroke();
        }
        for (let y = Math.floor(bounds.minY / gridSize) * gridSize; y <= bounds.maxY; y += gridSize) {
            ctx.beginPath();
            ctx.moveTo(bounds.minX, y);
            ctx.lineTo(bounds.maxX, y);
            ctx.stroke();
        }

        // Draw nodes
        nodes.forEach((n, index) => {
            const x = n.pos?.[0] ?? n.x ?? 0;
            const y = n.pos?.[1] ?? n.y ?? 0;
            const w = n.size?.[0] ?? n.width ?? 100;
            const h = n.size?.[1] ?? n.height ?? 60;
            
            ctx.fillStyle = getNodeColor(n);
            ctx.fillRect(x, y, w, h);
            
            ctx.strokeStyle = toRGBA(colors.inputText, 0.8);
            ctx.lineWidth = 1 / scale;
            ctx.strokeRect(x, y, w, h);

            if (scale > 0.3) {
                ctx.fillStyle = colors.inputText;
                ctx.font = `${Math.max(10, 12 / scale)}px Arial`;
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                const title = n.title || n.type || `Node ${index + 1}`;
                ctx.fillText(title.substring(0, 15), x + w / 2, y + h / 2);
            }
        });

        // Draw viewport indicator
        const app = getApp();
        if (app?.canvas?.ds) {
            const ds = app.canvas.ds;
            const mainCanvas = document.querySelector('canvas');
            
            if (mainCanvas) {
                const viewportX = -ds.offset[0];
                const viewportY = -ds.offset[1];
                const viewportW = mainCanvas.width / ds.scale;
                const viewportH = mainCanvas.height / ds.scale;

                ctx.fillStyle = toRGBA(colors.accent || '#4a90e2', 0.12);
                ctx.fillRect(viewportX, viewportY, viewportW, viewportH);

                ctx.strokeStyle = toRGBA(colors.accent || '#4a90e2', 0.8);
                ctx.lineWidth = 2 / scale;
                ctx.strokeRect(viewportX, viewportY, viewportW, viewportH);
            }
        }

        ctx.restore();
        panInfo.textContent = `Nodes: ${nodes.length} | Zoom: ${(zoom * 100).toFixed(0)}% | Pan: ${panX.toFixed(0)}, ${panY.toFixed(0)}`;
    }

    function navigateToPosition(canvasX, canvasY) {
        const worldPos = canvasToWorld(canvasX, canvasY);
        if (!worldPos) return;

        const app = getApp();
        const mainCanvas = document.querySelector('canvas');
        if (!app?.canvas?.ds || !mainCanvas) return;

        try {
            // Center the main canvas on the clicked world position
            app.canvas.ds.offset[0] = -worldPos.x + mainCanvas.width / 2;
            app.canvas.ds.offset[1] = -worldPos.y + mainCanvas.height / 2;
            app.canvas.setDirty(true, true);
            
            // Update minimap to reflect the change
            setTimeout(() => drawMinimap(), 50);
        } catch (err) {
            console.log("❌ Navigation error:", err);
        }
    }

    function isClickInViewport(canvasX, canvasY) {
        const app = getApp();
        if (!app?.canvas?.ds) return false;
        
        const ds = app.canvas.ds;
        const mainCanvas = document.querySelector('canvas');
        if (!mainCanvas) return false;
        
        const worldPos = canvasToWorld(canvasX, canvasY);
        if (!worldPos) return false;
        
        // Check if click is inside viewport rectangle in world coordinates
        const viewportX = -ds.offset[0];
        const viewportY = -ds.offset[1];
        const viewportW = mainCanvas.width / ds.scale;
        const viewportH = mainCanvas.height / ds.scale;
        
        return worldPos.x >= viewportX && worldPos.x <= viewportX + viewportW &&
               worldPos.y >= viewportY && worldPos.y <= viewportY + viewportH;
    }

    function adjustPanToKeepNodesVisible() {
        const nodes = getNodes();
        if (!nodes?.length) return;

        const canvas = currentDialog?.querySelector('canvas');
        if (!canvas) return;

        // Calculate bounds
        const bounds = nodes.reduce((acc, n) => {
            const x = n.pos?.[0] ?? n.x ?? 0;
            const y = n.pos?.[1] ?? n.y ?? 0;
            const w = n.size?.[0] ?? n.width ?? 100;
            const h = n.size?.[1] ?? n.height ?? 60;
            
            return {
                minX: Math.min(acc.minX, x),
                minY: Math.min(acc.minY, y),
                maxX: Math.max(acc.maxX, x + w),
                maxY: Math.max(acc.maxY, y + h)
            };
        }, { minX: Infinity, minY: Infinity, maxX: -Infinity, maxY: -Infinity });

        const width = bounds.maxX - bounds.minX;
        const height = bounds.maxY - bounds.minY;
        if (width <= 0 || height <= 0) return;

        const baseScale = Math.min(canvas.width / Math.max(width, 1000), canvas.height / Math.max(height, 1000));
        const scale = baseScale * zoom;

        // If zoomed in too much, adjust pan to keep nodes centered
        if (zoom > 2) {
            const maxPanX = canvas.width / 4;
            const maxPanY = canvas.height / 4;
            panX = Math.max(-maxPanX, Math.min(maxPanX, panX));
            panY = Math.max(-maxPanY, Math.min(maxPanY, panY));
        }
    }

    function setupEventHandlers() {
        const canvas = currentDialog.querySelector('canvas');
        let isViewportDragging = false;
        
        // Mouse handlers
        canvas.addEventListener('mousedown', (e) => {
            dragStartTime = Date.now();
            dragStartX = e.clientX;
            dragStartY = e.clientY;
            
            const rect = canvas.getBoundingClientRect();
            const canvasX = e.clientX - rect.left;
            const canvasY = e.clientY - rect.top;
            
            // Check if clicking inside viewport indicator
            isViewportDragging = isClickInViewport(canvasX, canvasY);
            
            if (isViewportDragging) {
                canvas.style.cursor = 'grab';
            }
        });

        canvas.addEventListener('mousemove', (e) => {
            if (!dragStartTime) return;
            
            const totalDelta = Math.abs(e.clientX - dragStartX) + Math.abs(e.clientY - dragStartY);
            
            if (totalDelta > DRAG_THRESHOLD && !isDragging) {
                isDragging = true;
                if (isViewportDragging) {
                    canvas.style.cursor = 'grabbing';
                } else {
                    canvas.style.cursor = 'move';
                }
            }
            
            if (isDragging) {
                if (isViewportDragging) {
                    // Move the viewport - convert movement to world coordinates
                    const app = getApp();
                    if (app?.canvas?.ds) {
                        const transform = getTransformState();
                        if (transform) {
                            // Scale movement by the inverse of the minimap scale
                            const movementScale = 1 / transform.scale;
                            app.canvas.ds.offset[0] -= e.movementX * movementScale;
                            app.canvas.ds.offset[1] -= e.movementY * movementScale;
                            app.canvas.setDirty(true, true);
                        }
                    }
                } else {
                    // Pan the minimap view
                    panX += e.movementX;
                    panY += e.movementY;
                }
                drawMinimap();
            }
        });

        canvas.addEventListener('mouseup', (e) => {
            const clickDuration = Date.now() - dragStartTime;
            const totalMovement = Math.abs(e.clientX - dragStartX) + Math.abs(e.clientY - dragStartY);
            
            if (!isDragging && clickDuration < 500 && totalMovement < DRAG_THRESHOLD) {
                if (!isViewportDragging) {
                    // Regular click-to-navigate (only if not clicking viewport)
                    const rect = canvas.getBoundingClientRect();
                    navigateToPosition(e.clientX - rect.left, e.clientY - rect.top);
                }
            }
            
            isDragging = false;
            isViewportDragging = false;
            dragStartTime = 0;
            canvas.style.cursor = 'crosshair';
        });

        canvas.addEventListener('wheel', (e) => {
            e.preventDefault();
            const oldZoom = zoom;
            zoom = Math.max(0.1, Math.min(5, zoom * (e.deltaY > 0 ? 0.9 : 1.1)));
            
            // Adjust pan to keep content centered when zooming
            if (zoom !== oldZoom) {
                adjustPanToKeepNodesVisible();
            }
            
            drawMinimap();
        });

        // Button handlers
        currentDialog.querySelector('#close-btn').onclick = () => closeDialog();
        currentDialog.querySelector('#legend-btn').onclick = () => {
            const legend = currentDialog.querySelector('.legend');
            const isVisible = legend.style.display !== 'none';
            legend.style.display = isVisible ? 'none' : 'block';
            if (!isVisible) updateLegend();
        };
        currentDialog.querySelector('#zoom-in').onclick = () => {
            zoom = Math.min(zoom * 1.2, 5);
            adjustPanToKeepNodesVisible();
            drawMinimap();
        };
        currentDialog.querySelector('#zoom-out').onclick = () => {
            zoom = Math.max(zoom / 1.2, 0.1);
            adjustPanToKeepNodesVisible();
            drawMinimap();
        };
        currentDialog.querySelector('#zoom-reset').onclick = () => {
            zoom = 1;
            panX = panY = 0;
            drawMinimap();
        };

        // ESC key
        const escHandler = (e) => e.key === 'Escape' && closeDialog();
        document.addEventListener('keydown', escHandler);
        
        return escHandler;
    }

    function createMinimapDialog() {
        if (currentDialog) return;

        const colors = getComfyUIColors();
        const { containerWidth, containerHeight, canvasWidth, canvasHeight } = calculateDimensions();

        // Clean up existing style
        document.getElementById('minimap-style')?.remove();

        // Create style tag
        const style = document.createElement('style');
        style.id = 'minimap-style';
        style.textContent = createStyleCSS(colors);
        document.head.appendChild(style);

        // Create container
        const container = document.createElement('div');
        container.id = 'endless-minimap';
        container.style.cssText = `
            position: fixed;
            top: 100px;
            right: 20px;
            width: ${containerWidth}px;
            height: ${containerHeight}px;
            background: ${colors.menu};
            color: ${colors.inputText};
            border: 1px solid ${colors.accent};
            border-radius: 8px;
            box-shadow: ${colors.shadow || '0 4px 12px rgba(0, 0, 0, 0.25)'};
            z-index: 99999;
            padding: 0;
            overflow: hidden;
            display: flex;
            flex-direction: column;
        `;

        container.innerHTML = `
            <div class="drag-bar">
                <span>Endless 🌊✨ Minimap</span>
                <div style="float: right; margin-top: -2px;">
                    <button id="legend-btn" title="Toggle legend">🎨</button>
                    <button id="zoom-out" title="Zoom out">▫️</button>
                    <button id="zoom-reset" title="Reset zoom and pan">🏠</button>
                    <button id="zoom-in" title="Zoom in">⬜</button>
                    <button id="close-btn" title="Close minimap">❌</button>
                </div>
            </div>
            <div style="flex: 1; position: relative; overflow: hidden;">
                <canvas width="${canvasWidth}" height="${canvasHeight}" style="display: block; cursor: crosshair; position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></canvas>
                <div class="legend"></div>
            </div>
            <div class="pan-info">Nodes: 0 | Zoom: 100% | Pan: 0, 0</div>
        `;

        document.body.appendChild(container);
        currentDialog = container;

        // Setup dragging
        makeDraggable(container, container.querySelector('.drag-bar'));

        // Setup event handlers
        const escHandler = setupEventHandlers();

        // Setup resize observer
        resizeObserver = new ResizeObserver(() => {
            const newAspectRatio = getCanvasAspectRatio();
            const canvas = container.querySelector('canvas');
            const currentAspectRatio = canvas.width / canvas.height;
            
            if (Math.abs(newAspectRatio - currentAspectRatio) > 0.1) {
                const { containerWidth: newContainerWidth, containerHeight: newContainerHeight, canvasWidth: newCanvasWidth, canvasHeight: newCanvasHeight } = calculateDimensions();
                
                // Update container size
                container.style.width = `${newContainerWidth}px`;
                container.style.height = `${newContainerHeight}px`;
                
                // Update canvas size
                canvas.width = newCanvasWidth;
                canvas.height = newCanvasHeight;
                
                drawMinimap();
            }
        });

        const mainCanvas = document.querySelector('canvas');
        if (mainCanvas) resizeObserver.observe(mainCanvas);
        resizeObserver.observe(document.body);

        // Setup theme updates
        unregisterThemeCallback = onThemeChange(updateTheme);

        // Start animation loop
        function updateLoop() {
            drawMinimap();
            animationId = setTimeout(updateLoop, 1000);
        }
        updateLoop();

        // Setup cleanup
        const originalRemove = container.remove.bind(container);
        container.remove = function() {
            clearTimeout(animationId);
            document.removeEventListener('keydown', escHandler);
            resizeObserver?.disconnect();
            unregisterThemeCallback?.();
            document.getElementById('minimap-style')?.remove();
            currentDialog = null;
            animationId = null;
            unregisterThemeCallback = null;
            resizeObserver = null;
            originalRemove();
        };
    }

    function closeDialog() {
        currentDialog?.remove();
    }

    // Register tool
    registerEndlessTool("Minimap", createMinimapDialog);
})();