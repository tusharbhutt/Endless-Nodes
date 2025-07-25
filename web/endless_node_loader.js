// ComfyUI Endless 🌊✨ Node Spawner - Optimized Version

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
        makeDraggable,
        addButtonHoverEffects
    } = window.EndlessHelpers;

    console.log("✅ Endless Node Spawner loaded.");

    // State management
    let currentDialog = null;
    let unregisterThemeCallback = null;
    let allNodesData = [];
    let currentFilter = '';
    let searchTimeout = null;
    let hoverTimeout = null;

    // Persistent data
    let recentlyUsedNodes = JSON.parse(localStorage.getItem('endlessNodeLoader_recentlyUsed') || '[]');
    let searchHistory = JSON.parse(localStorage.getItem('endlessNodeLoader_searchHistory') || '[]');

    // Constants
    const MAX_RECENT = 15;
    const MAX_HISTORY = 15;
    const DEFAULT_SPACING = { x: 300, y: 150 };
    const NODE_PADDING = 20;

    function createStyleCSS(colors) {
        return `
            .dialog-container {
                display: flex;
                flex-direction: column;
                height: 60vh;
                width: 35vw;
                min-width: 400px;
                min-height: 300px;
                background: ${colors.menu};
                color: ${colors.inputText};
                padding: 10px;
                border: 1px solid ${colors.border};
                border-radius: 8px;
                box-shadow: ${colors.shadow || '0 4px 20px rgba(0,0,0,0.5)'};
                z-index: 9999;
                overflow: hidden;
                box-sizing: border-box;
            }
            .dialog-title {
                margin: 0 0 15px 0;
                cursor: move;
                user-select: none;
                padding: 6px;
                background: ${colors.menuSecondary};
                color: ${colors.inputText};
                border-radius: 4px;
                font-size: 14px;
                border-bottom: 1px solid ${colors.border};
            }
            .filter-section {
                flex: 0 0 auto;
                display: flex;
                flex-direction: column;
                gap: 8px;
                margin-bottom: 8px;
                padding-bottom: 8px;
                border-bottom: 1px solid ${colors.border};
            }
            .filter-row {
                position: relative;
                display: flex;
                gap: 8px;
                align-items: center;
            }
            .filter-input {
                flex: 1;
                background: ${colors.inputBg};
                color: ${colors.inputText};
                border: 1px solid ${colors.border};
                border-radius: 4px;
                padding: 6px 8px;
                font-size: 12px;
            }
            .filter-input:focus {
                outline: none;
                border-color: ${colors.accent};
            }
            .expand-btn {
                background: ${colors.inputBg};
                color: ${colors.inputText};
                border: 1px solid ${colors.border};
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 12px;
                cursor: pointer;
            }
            .expand-btn:hover {
                background: ${colors.hoverBg};
                border-color: ${colors.accent};
            }
            .search-dropdown {
                position: absolute;
                top: 100%;
                left: 0;
                right: 80px;
                background: ${colors.menu};
                border: 1px solid ${colors.border};
                border-radius: 4px;
                max-height: 150px;
                overflow-y: auto;
                z-index: 10000;
                display: none;
            }
            .search-item {
                padding: 6px 8px;
                cursor: pointer;
                font-size: 12px;
                border-bottom: 1px solid ${colors.border};
            }
            .search-item:last-child { border-bottom: none; }
            .search-item:hover { background: ${colors.hoverBg}; }
            .counters {
                display: flex;
                justify-content: space-between;
                font-size: 11px;
                color: ${colors.descriptionText};
            }
            .counter-selected {
                color: ${colors.accent};
                font-weight: bold;
            }
            .recent-section {
                flex: 0 0 auto;
                display: flex;
                flex-wrap: wrap;
                gap: 6px;
                min-height: 30px;
                max-height: 15%;
                overflow-y: auto;
                border-bottom: 1px solid ${colors.border};
                padding-bottom: 6px;
                margin-bottom: 6px;
            }
            .recent-chip {
                background: ${toRGBA(colors.accent, 0.1)};
                color: ${colors.inputText};
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 11px;
                cursor: pointer;
                border: 1px solid transparent;
                transition: all 0.2s ease;
            }
            .recent-chip:hover {
                border-color: ${colors.accent};
                background: ${toRGBA(colors.accent, 0.2)};
            }
            .node-list {
                flex: 1 1 auto;
                overflow-y: auto;
                border-bottom: 1px solid ${colors.border};
                padding-bottom: 6px;
                margin-bottom: 6px;
            }
            .category {
                margin-bottom: 4px;
            }
            .category > summary {
                cursor: pointer;
                display: flex;
                align-items: center;
                gap: 8px;
                padding: 4px 0;
                list-style: none;
                color: ${colors.inputText};
            }
            .category > summary::-webkit-details-marker { display: none; }
            .category > summary::before {
                content: "▶";
                width: 12px;
                text-align: center;
                color: ${colors.descriptionText};
                font-size: 10px;
                transition: transform 0.2s ease;
            }
            .category[open] > summary::before {
                transform: rotate(90deg);
                color: ${colors.inputText};
            }
            .category > summary:hover {
                background: ${colors.hoverBg};
                border-radius: 4px;
            }
            .category ul {
                margin: 4px 0;
                padding-left: 1em;
            }
            .category li:hover {
                background: ${colors.hoverBg};
                border-radius: 4px;
            }
            .category input[type="checkbox"] {
                accent-color: ${colors.accent};
            }
            .cat-btn {
                background: ${colors.inputBg};
                color: ${colors.inputText};
                border: 1px solid ${colors.border};
                font-size: 10px;
                padding: 2px 6px;
                border-radius: 3px;
                cursor: pointer;
                transition: all 0.2s ease;
            }
            .cat-btn:hover {
                background: ${colors.hoverBg};
                border-color: ${colors.accent};
            }
            .cat-btn.select { background: ${toRGBA('#4CAF50', 0.1)}; }
            .cat-btn.deselect { background: ${toRGBA('#f44336', 0.1)}; }
            .footer {
                display: flex;
                justify-content: space-between;
                gap: 8px;
            }
            .btn-group {
                display: flex;
                gap: 8px;
            }
            .dialog-btn {
                background: ${colors.inputBg};
                color: ${colors.inputText};
                border: 1px solid ${colors.border};
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 12px;
                cursor: pointer;
                transition: all 0.2s ease;
            }
            .dialog-btn:hover {
                background: ${colors.hoverBg};
                border-color: ${colors.accent};
            }
            .dialog-btn.primary {
                background: ${toRGBA(colors.accent || '#4CAF50', 0.2)};
                border-color: ${colors.accent || '#4CAF50'};
            }
            .dialog-btn.secondary {
                background: ${toRGBA(colors.errorText || '#f44336', 0.2)};
                border-color: ${colors.errorText || '#f44336'};
            }
            .hidden { display: none !important; }
        `;
    }

    function updateTheme() {
        if (!currentDialog) return;
        
        const colors = getComfyUIColors();
        const styleTag = document.getElementById('node-loader-style');
        if (styleTag) {
            styleTag.textContent = createStyleCSS(colors);
        }
    }

    function getApp() {
        return window.app || window.comfyApp;
    }

    function getExistingNodePositions() {
        const app = getApp();
        const positions = [];
        
        if (app?.graph?.nodes) {
            app.graph.nodes.forEach(node => {
                if (node.pos) {
                    positions.push({
                        x: node.pos[0],
                        y: node.pos[1],
                        width: node.size?.[0] || 200,
                        height: node.size?.[1] || 100
                    });
                }
            });
        }
        return positions;
    }

    function findNonOverlappingPosition(startX, startY, width, height, existingPositions, spacingX, spacingY) {
        let x = startX;
        let y = startY;
        
        while (true) {
            let overlaps = false;
            
            for (const pos of existingPositions) {
                if (!(x + width + NODE_PADDING < pos.x || 
                      x - NODE_PADDING > pos.x + pos.width || 
                      y + height + NODE_PADDING < pos.y || 
                      y - NODE_PADDING > pos.y + pos.height)) {
                    overlaps = true;
                    break;
                }
            }
            
            if (!overlaps) return { x, y };
            
            x += spacingX;
            if (x > startX + spacingX * 5) {
                x = startX;
                y += spacingY;
            }
        }
    }

    function spawnNodes(types, spacingX = DEFAULT_SPACING.x, spacingY = DEFAULT_SPACING.y) {
        const app = getApp();
        if (!app?.graph?.add) {
            alert("ComfyUI graph not available.");
            return;
        }

        const startX = -app.canvas.ds.offset[0] + 50;
        const startY = -app.canvas.ds.offset[1] + 50;
        const existingPositions = getExistingNodePositions();
        
        const spawnedNodes = [];
        
        types.forEach((type, i) => {
            const node = LiteGraph.createNode(type);
            if (node) {
                const nodeWidth = node.size?.[0] || 200;
                const nodeHeight = node.size?.[1] || 100;
                
                const position = findNonOverlappingPosition(
                    startX + (i % 5) * spacingX,
                    startY + Math.floor(i / 5) * spacingY,
                    nodeWidth,
                    nodeHeight,
                    existingPositions,
                    spacingX,
                    spacingY
                );
                
                node.pos = [position.x, position.y];
                app.graph.add(node);
                spawnedNodes.push(type);
                
                existingPositions.push({
                    x: position.x,
                    y: position.y,
                    width: nodeWidth,
                    height: nodeHeight
                });
            } else {
                console.warn(`Could not create node: ${type}`);
            }
        });
        
        updateRecentlyUsedNodes(spawnedNodes);
        app.graph.setDirtyCanvas(true, true);
    }

    function updateRecentlyUsedNodes(newNodes) {
        newNodes.forEach(nodeType => {
            const index = recentlyUsedNodes.indexOf(nodeType);
            if (index > -1) recentlyUsedNodes.splice(index, 1);
            recentlyUsedNodes.unshift(nodeType);
        });
        
        recentlyUsedNodes = recentlyUsedNodes.slice(0, MAX_RECENT);
        localStorage.setItem('endlessNodeLoader_recentlyUsed', JSON.stringify(recentlyUsedNodes));
        
        if (currentDialog) updateRecentChips();
    }

    function updateRecentChips() {
        const recentSection = currentDialog.querySelector('.recent-section');
        if (!recentSection) return;
        
        recentSection.innerHTML = '';
        
        recentlyUsedNodes.forEach(nodeType => {
            const chip = document.createElement('button');
            chip.className = 'recent-chip';
            
            const nodeClass = LiteGraph.registered_node_types[nodeType];
            const displayName = nodeClass?.title || nodeClass?.name || nodeType.split("/").pop();
            chip.textContent = displayName;
            chip.title = nodeType;
            
            chip.onclick = () => {
                const checkbox = Array.from(currentDialog.querySelectorAll('.node-checkbox')).find(cb => {
                    return cb.closest('li').dataset.nodeType === nodeType;
                });
                if (checkbox) {
                    checkbox.checked = true;
                    updateSelectedCounter();
                }
            };
            
            recentSection.appendChild(chip);
        });
    }

    function addToSearchHistory(searchTerm) {
        if (!searchTerm.trim() || searchHistory.includes(searchTerm)) return;
        
        searchHistory.unshift(searchTerm);
        searchHistory = searchHistory.slice(0, MAX_HISTORY);
        localStorage.setItem('endlessNodeLoader_searchHistory', JSON.stringify(searchHistory));
    }

    function showSearchHistory(inputElement) {
        const dropdown = inputElement.parentElement.querySelector('.search-dropdown');
        if (!dropdown || searchHistory.length === 0) {
            if (dropdown) dropdown.style.display = 'none';
            return;
        }
        
        dropdown.innerHTML = '';
        searchHistory.forEach(term => {
            const item = document.createElement('div');
            item.className = 'search-item';
            item.textContent = term;
            item.onclick = () => {
                inputElement.value = term;
                applyFilter(term, true);
                hideSearchHistory(dropdown);
            };
            dropdown.appendChild(item);
        });
        
        dropdown.style.display = 'block';
        
        setTimeout(() => {
            if (dropdown.style.display === 'block') {
                hideSearchHistory(dropdown);
            }
        }, 10000);
    }

    function hideSearchHistory(dropdown) {
        dropdown.style.display = 'none';
    }

    function applyFilter(filterText, saveToHistory = true) {
        currentFilter = filterText.toLowerCase();
        const nodeList = currentDialog.querySelector('.node-list');
        
        if (!currentFilter) {
            nodeList.querySelectorAll('.category, .category li').forEach(el => {
                el.classList.remove('hidden');
            });
            updateTotalCounter();
            return;
        }
        
        nodeList.querySelectorAll('.category').forEach(details => {
            const categoryName = details.querySelector('summary span').textContent.toLowerCase();
            const categoryMatches = categoryName.includes(currentFilter);
            
            let hasMatchingNodes = false;
            const nodeItems = details.querySelectorAll('li');
            
            nodeItems.forEach(li => {
                const nodeText = li.textContent.toLowerCase();
                const nodeType = li.dataset.nodeType?.toLowerCase() || '';
                const matches = nodeText.includes(currentFilter) || nodeType.includes(currentFilter);
                
                if (matches) {
                    li.classList.remove('hidden');
                    hasMatchingNodes = true;
                } else {
                    li.classList.add('hidden');
                }
            });
            
            if (categoryMatches || hasMatchingNodes) {
                details.classList.remove('hidden');
                if (hasMatchingNodes && !categoryMatches) {
                    details.open = true;
                }
            } else {
                details.classList.add('hidden');
            }
        });
        
        updateTotalCounter();
    }

    function updateSelectedCounter() {
        const counter = currentDialog.querySelector('.counter-selected');
        if (!counter) return;
        
        const checkedBoxes = currentDialog.querySelectorAll('.node-checkbox:checked');
        counter.textContent = `Selected: ${checkedBoxes.length}`;
    }

    function updateTotalCounter() {
        const counter = currentDialog.querySelector('.counter-total');
        if (!counter) return;
        
        const visibleNodes = currentDialog.querySelectorAll('.category li:not(.hidden)');
        counter.textContent = `Total: ${visibleNodes.length}/${allNodesData.length}`;
    }

    function toggleAllCategories(expand) {
        const details = currentDialog.querySelectorAll('.category:not(.hidden)');
        details.forEach(detail => {
            detail.open = expand;
        });
    }

    function buildHierarchy(nodes) {
        const root = {};
        nodes.forEach(n => {
            let current = root;
            n.pathParts.forEach((part, idx) => {
                if (!current[part]) {
                    current[part] = { _nodes: [], _subcategories: {} };
                }
                if (idx === n.pathParts.length - 1) {
                    current[part]._nodes.push(n);
                } else {
                    current = current[part]._subcategories;
                }
            });
        });
        return root;
    }

    function countNodesInCategory(categoryObj) {
        let count = categoryObj._nodes?.length || 0;
        if (categoryObj._subcategories) {
            Object.values(categoryObj._subcategories).forEach(sub => {
                count += countNodesInCategory(sub);
            });
        }
        return count;
    }

    function selectAllInCategory(categoryDetails, select = true) {
        const checkboxes = categoryDetails.querySelectorAll("input[type='checkbox']");
        checkboxes.forEach(checkbox => {
            checkbox.checked = select;
        });
        updateSelectedCounter();
    }

    function renderCategory(categoryObj, depth = 0) {
        return Object.entries(categoryObj)
            .sort(([a], [b]) => a.localeCompare(b))
            .map(([cat, obj]) => {
                const totalNodes = countNodesInCategory(obj);

                const details = document.createElement("details");
                details.className = "category";
                details.style.paddingLeft = `${depth * 1.2}em`;

                const summary = document.createElement("summary");
                
                const categoryName = document.createElement("span");
                categoryName.textContent = `${cat} (${totalNodes})`;

                const selectAllBtn = document.createElement("button");
                selectAllBtn.textContent = "All";
                selectAllBtn.className = "cat-btn select";
                selectAllBtn.onclick = (e) => {
                    e.stopPropagation();
                    selectAllInCategory(details, true);
                };

                const selectNoneBtn = document.createElement("button");
                selectNoneBtn.textContent = "None";
                selectNoneBtn.className = "cat-btn deselect";
                selectNoneBtn.onclick = (e) => {
                    e.stopPropagation();
                    selectAllInCategory(details, false);
                };

                summary.appendChild(categoryName);
                summary.appendChild(selectAllBtn);
                summary.appendChild(selectNoneBtn);
                details.appendChild(summary);

                const list = document.createElement("ul");
                (obj._nodes || []).forEach(node => {
                    const li = document.createElement("li");
                    li.dataset.nodeType = node.type;
                    
                    const checkbox = document.createElement("input");
                    checkbox.type = "checkbox";
                    checkbox.className = "node-checkbox";
                    checkbox.onchange = updateSelectedCounter;
                    
                    const label = document.createElement("label");
                    label.textContent = node.displayName;

                    li.appendChild(checkbox);
                    li.appendChild(label);
                    list.appendChild(li);
                });

                details.appendChild(list);

                const subCategories = renderCategory(obj._subcategories || {}, depth + 1);
                subCategories.forEach(sub => details.appendChild(sub));

                return details;
            });
    }

    function getSelectedNodeTypes() {
        const selected = [];
        currentDialog.querySelectorAll('.node-checkbox:checked').forEach(checkbox => {
            const nodeType = checkbox.closest('li').dataset.nodeType;
            if (nodeType) selected.push(nodeType);
        });
        return selected;
    }

    function clearSelectedNodes() {
        currentDialog.querySelectorAll('.node-checkbox:checked').forEach(checkbox => {
            checkbox.checked = false;
        });
        updateSelectedCounter();
    }

    function setupEventHandlers() {
        const filterInput = currentDialog.querySelector('.filter-input');
        const searchDropdown = currentDialog.querySelector('.search-dropdown');
        const expandBtn = currentDialog.querySelector('.expand-btn');
        
        let isExpanded = false;

        // Filter input handlers
        filterInput.oninput = (e) => applyFilter(e.target.value, false);
        
        filterInput.onkeydown = (e) => {
            if (e.key === 'Enter' && e.target.value.trim()) {
                addToSearchHistory(e.target.value.trim());
                hideSearchHistory(searchDropdown);
            } else if (e.key === 'ArrowDown' && searchHistory.length > 0) {
                showSearchHistory(filterInput);
                e.preventDefault();
            }
        };

        filterInput.onfocus = (e) => {
            if (!e.target.value.trim()) {
                showSearchHistory(filterInput);
            }
        };

        filterInput.onblur = (e) => {
            if (e.target.value.trim()) {
                addToSearchHistory(e.target.value.trim());
            }
            if (hoverTimeout) {
                clearTimeout(hoverTimeout);
                hoverTimeout = null;
            }
            setTimeout(() => hideSearchHistory(searchDropdown), 150);
        };

        filterInput.onmouseenter = () => {
            if (searchTimeout) {
                clearTimeout(searchTimeout);
                searchTimeout = null;
            }
            
            hoverTimeout = setTimeout(() => {
                if (searchHistory.length > 0) {
                    showSearchHistory(filterInput);
                }
            }, 1000);
        };

        filterInput.onmouseleave = () => {
            if (hoverTimeout) {
                clearTimeout(hoverTimeout);
                hoverTimeout = null;
            }
            
            searchTimeout = setTimeout(() => {
                hideSearchHistory(searchDropdown);
            }, 10000);
        };

        // Expand button
        expandBtn.onclick = () => {
            isExpanded = !isExpanded;
            toggleAllCategories(isExpanded);
            expandBtn.textContent = isExpanded ? "Collapse All" : "Expand All";
        };

        // Button handlers
        currentDialog.querySelector('#spawn-btn').onclick = () => {
            const selectedTypes = getSelectedNodeTypes();
            if (selectedTypes.length === 0) {
                alert("Please select at least one node to spawn.");
                return;
            }
            spawnNodes(selectedTypes);
            closeDialog();
        };

        currentDialog.querySelector('#clear-btn').onclick = clearSelectedNodes;
        currentDialog.querySelector('#cancel-btn').onclick = closeDialog;
        currentDialog.querySelector('#clear-history-btn').onclick = () => {
            searchHistory = [];
            localStorage.setItem('endlessNodeLoader_searchHistory', JSON.stringify(searchHistory));
            const dropdown = currentDialog.querySelector('.search-dropdown');
            if (dropdown) dropdown.style.display = 'none';
        };
        currentDialog.querySelector('#clear-recent-btn').onclick = () => {
            recentlyUsedNodes = [];
            localStorage.setItem('endlessNodeLoader_recentlyUsed', JSON.stringify(recentlyUsedNodes));
            updateRecentChips(); // This will clear the chips
        };

        // ESC key handler
        const escHandler = (e) => e.key === 'Escape' && closeDialog();
        document.addEventListener('keydown', escHandler);
        
        return escHandler;
    }

    function createNodeLoaderDialog() {
        if (currentDialog) return;

        const colors = getComfyUIColors();

        // Clean up existing style
        document.getElementById('node-loader-style')?.remove();

        // Create style tag
        const style = document.createElement('style');
        style.id = 'node-loader-style';
        style.textContent = createStyleCSS(colors);
        document.head.appendChild(style);

        // Create container
        const container = document.createElement("div");
        // Calculate max size based on viewport
        const maxWidth = Math.min(window.innerWidth * 0.4, 1536); // 40% of window width, max 1536px
        const maxHeight = Math.min(window.innerHeight * 0.6, 1296); // 60% of window height, max 1296px

        container.className = "dialog-container";
        container.style.cssText = `
            position: fixed;
            top: 10%;
            left: 50%;
            transform: translateX(-50%);
            max-width: ${maxWidth}px;
            max-height: ${maxHeight}px;
        `;

        container.innerHTML = `
            <h3 class="dialog-title"> Endless 🌊✨ Node Spawner Drag Bar</h3>
            
            <div class="filter-section">
                <div class="filter-row">
                    <input type="text" class="filter-input" placeholder="Filter nodes..." title="Type to filter nodes, ↓ for history">
                    <div class="search-dropdown"></div>
                    <button class="expand-btn" title="Expand/collapse all categories">Expand All</button>
                </div>
                <div class="counters">
                    <span class="counter-selected">Selected: 0</span>
                    <span class="counter-total">Total: 0</span>
                </div>
            </div>

            <div class="recent-section"></div>
            <div class="node-list"></div>

            <div class="footer">
                <div class="btn-group">
                    <button id="spawn-btn" class="dialog-btn primary" title="Spawn selected nodes">🌊 Spawn Nodes</button>
                    <button id="clear-btn" class="dialog-btn" title="Clear all selections">Clear Selected</button>
                </div>
                <div class="btn-group">
                    <button id="clear-history-btn" class="dialog-btn" title="Clear search history">Clear Search</button>
                    <button id="clear-recent-btn" class="dialog-btn" title="Clear recent nodes">Clear Recent</button>
                    <button id="cancel-btn" class="dialog-btn secondary" title="Close dialog">❌ Cancel</button>
                </div>
            </div>
        `;

        document.body.appendChild(container);
        currentDialog = container;

        // Setup dragging
        makeDraggable(container, container.querySelector('.dialog-title'));

        // Build node data
        const nodes = Object.entries(LiteGraph.registered_node_types)
            .filter(([key, value]) => key && value)
            .map(([type, nodeClass]) => {
                const category = nodeClass.category || "Other";
                const displayName = nodeClass.title || nodeClass.name || type.split("/").pop();
                return {
                    type,
                    category,
                    pathParts: category.split("/"),
                    displayName,
                    description: nodeClass.desc || nodeClass.description || "",
                    fullPath: category + "/" + displayName
                };
            })
            .sort((a, b) => a.category.localeCompare(b.category) || a.displayName.localeCompare(b.displayName));

        allNodesData = nodes;
        
        // Render hierarchy
        const hierarchy = buildHierarchy(nodes);
        const tree = renderCategory(hierarchy);
        const nodeList = container.querySelector('.node-list');
        tree.forEach(section => nodeList.appendChild(section));

        // Add hover effects
        addButtonHoverEffects(container);

        // Setup event handlers
        const escHandler = setupEventHandlers();

        // Setup theme updates
        unregisterThemeCallback = onThemeChange(updateTheme);

        // Initialize
        updateRecentChips();
        updateSelectedCounter();
        updateTotalCounter();
        
        // Focus filter input
        container.querySelector('.filter-input').focus();

        // Setup cleanup
        const originalRemove = container.remove.bind(container);
        container.remove = function() {
            document.removeEventListener('keydown', escHandler);
            unregisterThemeCallback?.();
            document.getElementById('node-loader-style')?.remove();
            if (searchTimeout) clearTimeout(searchTimeout);
            if (hoverTimeout) clearTimeout(hoverTimeout);
            currentDialog = null;
            unregisterThemeCallback = null;
            searchTimeout = null;
            hoverTimeout = null;
            originalRemove();
        };
    }

    function closeDialog() {
        currentDialog?.remove();
    }

    // Register tool
    registerEndlessTool("Node Spawner", createNodeLoaderDialog);
})();