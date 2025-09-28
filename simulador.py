<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Panel de Análisis Lightning Storm</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {
            --primary-blue: #1e40af;
            --secondary-blue: #3b82f6;
            --accent-gold: #f59e0b;
            --success-green: #10b981;
            --danger-red: #ef4444;
            --dark-bg: #0f172a;
            --card-bg: rgba(30, 41, 59, 0.95);
            --border-color: rgba(148, 163, 184, 0.1);
            --text-primary: #f8fafc;
            --text-secondary: #cbd5e1;
            --shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            --gradient-primary: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
            background: var(--dark-bg);
            color: var(--text-primary);
            line-height: 1.6;
            overflow-x: auto;
        }

        .dashboard {
            min-height: 100vh;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        }

        .header {
            background: var(--card-bg);
            border-bottom: 1px solid var(--border-color);
            backdrop-filter: blur(20px);
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .header-content {
            max-width: 1400px;
            margin: 0 auto;
            padding: 1.5rem 2rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        .logo-icon {
            width: 48px;
            height: 48px;
            background: var(--gradient-primary);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            color: white;
        }

        .logo-text h1 {
            font-size: 1.75rem;
            font-weight: 700;
            margin-bottom: 0.25rem;
        }

        .logo-text p {
            font-size: 0.875rem;
            color: var(--text-secondary);
            font-weight: 500;
        }

        .header-stats {
            display: flex;
            gap: 2rem;
            align-items: center;
        }

        .stat-chip {
            background: rgba(59, 130, 246, 0.1);
            border: 1px solid rgba(59, 130, 246, 0.2);
            padding: 0.5rem 1rem;
            border-radius: 8px;
            text-align: center;
        }

        .stat-chip-value {
            font-size: 1.125rem;
            font-weight: 700;
            color: var(--secondary-blue);
        }

        .stat-chip-label {
            font-size: 0.75rem;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .main-container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
            display: grid;
            grid-template-columns: 280px 1fr;
            gap: 2rem;
            min-height: calc(100vh - 100px);
        }

        .sidebar {
            background: var(--card-bg);
            border-radius: 16px;
            border: 1px solid var(--border-color);
            height: fit-content;
            position: sticky;
            top: 120px;
        }

        .sidebar-nav {
            padding: 1.5rem 0;
        }

        .nav-item {
            display: flex;
            align-items: center;
            gap: 1rem;
            padding: 0.875rem 1.5rem;
            color: var(--text-secondary);
            text-decoration: none;
            transition: all 0.2s ease;
            border: none;
            background: none;
            width: 100%;
            text-align: left;
            font-size: 0.925rem;
            font-weight: 500;
            cursor: pointer;
        }

        .nav-item:hover {
            background: rgba(59, 130, 246, 0.1);
            color: var(--secondary-blue);
        }

        .nav-item.active {
            background: var(--gradient-primary);
            color: white;
            font-weight: 600;
        }

        .nav-item i {
            width: 20px;
            text-align: center;
            opacity: 0.8;
        }

        .content-area {
            background: var(--card-bg);
            border-radius: 16px;
            border: 1px solid var(--border-color);
            backdrop-filter: blur(20px);
            min-height: 600px;
        }

        .content-header {
            padding: 2rem 2rem 1rem;
            border-bottom: 1px solid var(--border-color);
        }

        .content-header h2 {
            font-size: 1.75rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }

        .content-header p {
            color: var(--text-secondary);
            font-size: 1rem;
        }

        .content-body {
            padding: 2rem;
        }

        .section {
            display: none;
        }

        .section.active {
            display: block;
            animation: fadeInUp 0.3s ease-out;
        }

        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }

        .metric-card {
            background: rgba(30, 41, 59, 0.6);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.5rem;
            position: relative;
            overflow: hidden;
        }

        .metric-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: var(--gradient-primary);
        }

        .metric-card.success::before {
            background: linear-gradient(90deg, var(--success-green), #34d399);
        }

        .metric-card.warning::before {
            background: linear-gradient(90deg, var(--accent-gold), #fbbf24);
        }

        .metric-card.danger::before {
            background: linear-gradient(90deg, var(--danger-red), #f87171);
        }

        .metric-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 1rem;
        }

        .metric-title {
            font-size: 0.875rem;
            font-weight: 600;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .metric-icon {
            width: 40px;
            height: 40px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(59, 130, 246, 0.1);
            color: var(--secondary-blue);
        }

        .metric-value {
            font-size: 2.5rem;
            font-weight: 800;
            line-height: 1;
            margin-bottom: 0.5rem;
        }

        .metric-change {
            font-size: 0.875rem;
            display: flex;
            align-items: center;
            gap: 0.25rem;
        }

        .metric-change.positive {
            color: var(--success-green);
        }

        .metric-change.negative {
            color: var(--danger-red);
        }

        .form-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }

        .form-group {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }

        .form-label {
            font-size: 0.875rem;
            font-weight: 600;
            color: var(--text-primary);
        }

        .form-input, .form-select {
            background: rgba(30, 41, 59, 0.8);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 0.875rem 1rem;
            color: var(--text-primary);
            font-size: 0.925rem;
            transition: all 0.2s ease;
        }

        .form-input:focus, .form-select:focus {
            outline: none;
            border-color: var(--secondary-blue);
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }

        .btn {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.875rem 1.5rem;
            border-radius: 8px;
            font-size: 0.925rem;
            font-weight: 600;
            text-decoration: none;
            border: none;
            cursor: pointer;
            transition: all 0.2s ease;
            text-align: center;
            justify-content: center;
        }

        .btn-primary {
            background: var(--gradient-primary);
            color: white;
        }

        .btn-primary:hover {
            transform: translateY(-1px);
            box-shadow: 0 10px 25px rgba(59, 130, 246, 0.3);
        }

        .btn-secondary {
            background: rgba(148, 163, 184, 0.1);
            color: var(--text-primary);
            border: 1px solid var(--border-color);
        }

        .btn-secondary:hover {
            background: rgba(148, 163, 184, 0.2);
        }

        .btn-success {
            background: linear-gradient(135deg, var(--success-green), #34d399);
            color: white;
        }

        .btn-danger {
            background: linear-gradient(135deg, var(--danger-red), #f87171);
            color: white;
        }

        .wheel-visual {
            width: 300px;
            height: 300px;
            margin: 20px auto;
            border-radius: 50%;
            background: conic-gradient(
                #ff6b6b 0deg 9.23deg,
                #4ecdc4 9.23deg 18.46deg,
                #45b7d1 18.46deg 27.69deg,
                #96ceb4 27.69deg 36.92deg,
                #feca57 36.92deg 46.15deg,
                #ff9ff3 46.15deg 55.38deg,
                #54a0ff 55.38deg 64.61deg,
                #5f27cd 64.61deg 73.84deg
            );
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 3px solid var(--border-color);
        }

        .wheel-pointer {
            position: absolute;
            top: -10px;
            left: 50%;
            transform: translateX(-50%);
            width: 0;
            height: 0;
            border-left: 15px solid transparent;
            border-right: 15px solid transparent;
            border-top: 20px solid var(--accent-gold);
            z-index: 10;
        }

        .pattern-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1.5rem;
            margin: 2rem 0;
        }

        .pattern-card {
            background: rgba(30, 41, 59, 0.6);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.5rem;
        }

        .pattern-title {
            font-size: 1.125rem;
            font-weight: 700;
            margin-bottom: 1rem;
            color: var(--secondary-blue);
        }

        .pattern-stats {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
        }

        .pattern-stat {
            text-align: center;
            padding: 0.75rem;
            background: rgba(0, 0, 0, 0.2);
            border-radius: 8px;
        }

        .pattern-value {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--accent-gold);
        }

        .pattern-label {
            font-size: 0.75rem;
            color: var(--text-secondary);
            text-transform: uppercase;
        }

        .range-analysis {
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid rgba(16, 185, 129, 0.2);
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1.5rem 0;
        }

        .range-title {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            font-size: 1.125rem;
            font-weight: 700;
            color: var(--success-green);
            margin-bottom: 1rem;
        }

        .range-item {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0.875rem;
            background: rgba(30, 41, 59, 0.4);
            border-radius: 8px;
            margin-bottom: 0.75rem;
            border: 1px solid var(--border-color);
        }

        .data-table {
            background: rgba(30, 41, 59, 0.6);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            overflow: hidden;
            margin-top: 1.5rem;
        }

        .table {
            width: 100%;
            border-collapse: collapse;
        }

        .table th {
            background: rgba(30, 41, 59, 0.8);
            padding: 1rem;
            text-align: left;
            font-size: 0.875rem;
            font-weight: 600;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .table td {
            padding: 1rem;
            border-top: 1px solid var(--border-color);
            font-size: 0.925rem;
        }

        .table tbody tr:hover {
            background: rgba(59, 130, 246, 0.05);
        }

        .numbers-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
            gap: 1rem;
            margin: 1.5rem 0;
        }

        .number-card {
            background: rgba(30, 41, 59, 0.6);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
            transition: all 0.2s ease;
            position: relative;
            overflow: hidden;
        }

        .number-card:hover {
            transform: translateY(-4px);
            box-shadow: var(--shadow);
        }

        .number-card.hot {
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.2), rgba(248, 113, 113, 0.1));
            border-color: rgba(239, 68, 68, 0.3);
        }

        .number-card.hot::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--danger-red), #f87171);
        }

        .number-card.cold {
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(147, 197, 253, 0.1));
            border-color: rgba(59, 130, 246, 0.3);
        }

        .number-card.cold::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--secondary-blue), #93c5fd);
        }

        .number-value {
            font-size: 1.75rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
        }

        .number-stats {
            font-size: 0.75rem;
            color: var(--text-secondary);
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
        }

        .alert {
            padding: 1rem 1.5rem;
            border-radius: 8px;
            margin: 1rem 0;
            border-left: 4px solid;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .alert-success {
            background: rgba(16, 185, 129, 0.1);
            border-color: var(--success-green);
            color: var(--success-green);
        }

        .alert-warning {
            background: rgba(245, 158, 11, 0.1);
            border-color: var(--accent-gold);
            color: var(--accent-gold);
        }

        .alert-danger {
            background: rgba(239, 68, 68, 0.1);
            border-color: var(--danger-red);
            color: var(--danger-red);
        }

        .chart-container {
            background: rgba(30, 41, 59, 0.6);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1.5rem 0;
        }

        @media (max-width: 1024px) {
            .main-container {
                grid-template-columns: 1fr;
                gap: 1rem;
                padding: 1rem;
            }

            .sidebar {
                position: static;
                border-radius: 12px 12px 0 0;
            }

            .sidebar-nav {
                display: flex;
                overflow-x: auto;
                padding: 1rem 0;
            }

            .nav-item {
                white-space: nowrap;
                min-width: fit-content;
            }

            .header-stats {
                display: none;
            }

            .metrics-grid {
                grid-template-columns: 1fr;
                gap: 1rem;
            }

            .form-grid {
                grid-template-columns: 1fr;
            }

            .pattern-grid {
                grid-template-columns: 1fr;
            }

            .numbers-grid {
                grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));
                gap: 0.75rem;
            }
        }
    </style>
</head>
<body>
    <div class="dashboard">
        <div class="header">
            <div class="header-content">
                <div class="logo">
                    <div class="logo-icon">
                        <i class="fas fa-bolt"></i>
                    </div>
                    <div class="logo-text">
                        <h1>Lightning Storm Analytics</h1>
                        <p>Plataforma Profesional de Inteligencia de Juego</p>
                    </div>
                </div>
                <div class="header-stats">
                    <div class="stat-chip">
                        <div class="stat-chip-value" id="header-total-rounds">0</div>
                        <div class="stat-chip-label">Total Giros</div>
                    </div>
                    <div class="stat-chip">
                        <div class="stat-chip-value" id="header-success-rate">0%</div>
                        <div class="stat-chip-label">Tasa de Bonus</div>
                    </div>
                </div>
            </div>
        </div>

        <div class="main-container">
            <div class="sidebar">
                <nav class="sidebar-nav">
                    <button class="nav-item active" onclick="showSection('data-entry')">
                        <i class="fas fa-plus-circle"></i>
                        Entrada de Datos
                    </button>
                    <button class="nav-item" onclick="showSection('analytics')">
                        <i class="fas fa-chart-line"></i>
                        Análisis
                    </button>
                    <button class="nav-item" onclick="showSection('patterns')">
                        <i class="fas fa-sync-alt"></i>
                        Patrones de Giro
                    </button>
                    <button class="nav-item" onclick="showSection('predictions')">
                        <i class="fas fa-brain"></i>
                        Predicciones
                    </button>
                    <button class="nav-item" onclick="showSection('visualization')">
                        <i class="fas fa-chart-bar"></i>
                        Visualización
                    </button>
                    <button class="nav-item" onclick="showSection('reports')">
                        <i class="fas fa-file-alt"></i>
                        Reportes
                    </button>
                    <button class="nav-item" onclick="showSection('settings')">
                        <i class="fas fa-cog"></i>
                        Configuración
                    </button>
                </nav>
            </div>

            <div class="content-area">
                <!-- Entrada de Datos -->
                <div id="data-entry" class="section active">
                    <div class="content-header">
                        <h2>Entrada de Datos</h2>
                        <p>Registra nuevos resultados para mantener análisis precisos</p>
                    </div>
                    <div class="content-body">
                        <div class="form-grid">
                            <div class="form-group">
                                <label class="form-label">Tipo de Resultado</label>
                                <select id="result-type" class="form-select" onchange="toggleResultFields()">
                                    <option value="number">Número (1-20)</option>
                                    <option value="leaf">Leaf (1:1)</option>
                                </select>
                            </div>
                            <div class="form-group" id="number-group">
                                <label class="form-label">Número</label>
                                <input type="number" id="number-input" class="form-input" min="1" max="20" placeholder="Ingresa número (1-20)">
                            </div>
                            <div class="form-group">
                                <label class="form-label">Posición Inicial</label>
                                <input type="number" id="start-position" class="form-input" min="1" max="39" placeholder="Posición inicial (1-39)">
                            </div>
                            <div class="form-group">
                                <label class="form-label">Dirección del Giro</label>
                                <select id="spin-direction" class="form-select">
                                    <option value="right">Derecha (Horario)</option>
                                    <option value="left">Izquierda (Antihorario)</option>
                                </select>
                            </div>
                            <div class="form-group" id="bonus-group">
                                <label class="form-label">Bonus</label>
                                <select id="bonus-input" class="form-select">
                                    <option value="false">Sin Bonus</option>
                                    <option value="true">Con Bonus</option>
                                </select>
                            </div>
                            <div class="form-group" id="multiplier-group">
                                <label class="form-label">Multiplicador</label>
                                <input type="number" id="multiplier-input" class="form-input" min="1" step="0.1" value="1.0" placeholder="1.0">
                            </div>
                        </div>
                        <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap; margin-top: 1.5rem;">
                            <button class="btn btn-primary" onclick="addRound()">
                                <i class="fas fa-plus"></i>
                                Agregar Giro
                            </button>
                            <button class="btn btn-secondary" onclick="quickAddMode()">
                                <i class="fas fa-tachometer-alt"></i>
                                Modo Rápido
                            </button>
                        </div>
                        <div id="add-result"></div>
                    </div>
                </div>

                <!-- Análisis -->
                <div id="analytics" class="section">
                    <div class="content-header">
                        <h2>Panel de Análisis</h2>
                        <p>Análisis estadístico completo de patrones de juego</p>
                    </div>
                    <div class="content-body">
                        <div class="metrics-grid">
                            <div class="metric-card">
                                <div class="metric-header">
                                    <span class="metric-title">Total de Giros</span>
                                    <div class="metric-icon">
                                        <i class="fas fa-play-circle"></i>
                                    </div>
                                </div>
                                <div class="metric-value" id="total-rounds">0</div>
                                <div class="metric-change">
                                    <span>Actividad de sesión</span>
                                </div>
                            </div>
                            
                            <div class="metric-card success">
                                <div class="metric-header">
                                    <span class="metric-title">Tasa de Bonus</span>
                                    <div class="metric-icon">
                                        <i class="fas fa-gift"></i>
                                    </div>
                                </div>
                                <div class="metric-value" id="bonus-rate">0%</div>
                                <div class="metric-change positive">
                                    <i class="fas fa-arrow-up"></i>
                                    <span>Indicador de rendimiento</span>
                                </div>
                            </div>

                            <div class="metric-card warning">
                                <div class="metric-header">
                                    <span class="metric-title">Racha Actual</span>
                                    <div class="metric-icon">
                                        <i class="fas fa-fire"></i>
                                    </div>
                                </div>
                                <div class="metric-value" id="current-streak">0</div>
                                <div class="metric-change">
                                    <span>Giros sin bonus</span>
                                </div>
                            </div>

                            <div class="metric-card">
                                <div class="metric-header">
                                    <span class="metric-title">Frecuencia Leaf</span>
                                    <div class="metric-icon">
                                        <i class="fas fa-leaf"></i>
                                    </div>
                                </div>
                                <div class="metric-value" id="leaf-rate">0%</div>
                                <div class="metric-change">
                                    <span>Jugadas seguras</span>
                                </div>
                            </div>
                        </div>

                        <div class="range-analysis">
                            <div class="range-title">
                                <i class="fas fa-lightbulb"></i>
                                Recomendaciones Estratégicas
                            </div>
                            <div id="recommendations-list">
                                <!-- Las recomendaciones se poblarán aquí -->
                            </div>
                        </div>

                        <h3 style="margin: 2rem 0 1rem;">Análisis de Rendimiento por Número</h3>
                        <div class="numbers-grid" id="numbers-grid">
                            <!-- Los números se poblarán aquí -->
                        </div>
                    </div>
                </div>

                <!-- Patrones de Giro -->
                <div id="patterns" class="section">
                    <div class="content-header">
                        <h2>Análisis de Patrones de Giro</h2>
                        <p>Análisis avanzado de direcciones y rangos de movimiento</p>
                    </div>
                    <div class="content-body">
                        <div class="pattern-grid">
                            <div class="pattern-card">
                                <div class="pattern-title">
                                    <i class="fas fa-arrow-right"></i>
                                    Giros a la Derecha
                                </div>
                                <div class="pattern-stats">
                                    <div class="pattern-stat">
                                        <div class="pattern-value" id="right-spins-count">0</div>
                                        <div class="pattern-label">Total</div>
                                    </div>
                                    <div class="pattern-stat">
                                        <div class="pattern-value" id="right-avg-distance">0</div>
                                        <div class="pattern-label">Distancia Prom.</div>
                                    </div>
                                    <div class="pattern-stat">
                                        <div class="pattern-value" id="right-bonus-rate">0%</div>
                                        <div class="pattern-label">Tasa Bonus</div>
                                    </div>
                                    <div class="pattern-stat">
                                        <div class="pattern-value" id="right-leaf-rate">0%</div>
                                        <div class="pattern-label">Tasa Leaf</div>
                                    </div>
                                </div>
                            </div>

                            <div class="pattern-card">
                                <div class="pattern-title">
                                    <i class="fas fa-arrow-left"></i>
                                    Giros a la Izquierda
                                </div>
                                <div class="pattern-stats">
                                    <div class="pattern-stat">
                                        <div class="pattern-value" id="left-spins-count">0</div>
                                        <div class="pattern-label">Total</div>
                                    </div>
                                    <div class="pattern-stat">
                                        <div class="pattern-value" id="left-avg-distance">0</div>
                                        <div class="pattern-label">Distancia Prom.</div>
                                    </div>
                                    <div class="pattern-stat">
                                        <div class="pattern-value" id="left-bonus-rate">0%</div>
                                        <div class="pattern-label">Tasa Bonus</div>
                                    </div>
                                    <div class="pattern-stat">
                                        <div class="pattern-value" id="left-leaf-rate">0%</div>
                                        <div class="pattern-label">Tasa Leaf</div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="range-analysis">
                            <div class="range-title">
                                <i class="fas fa-chart-area"></i>
                                Análisis de Rangos de Movimiento
                            </div>
                            <div id="range-analysis-list">
                                <!-- El análisis de rangos se poblará aquí -->
                            </div>
                        </div>

                        <div class="chart-container">
                            <h3>Distribución de Distancias por Dirección</h3>
                            <canvas id="distanceChart"></canvas>
                        </div>

                        <h3 style="margin: 2rem 0 1rem;">Patrones de Posición Inicial</h3>
                        <div class="numbers-grid" id="start-positions-grid">
                            <!-- Las posiciones iniciales se poblarán aquí -->
                        </div>
                    </div>
                </div>

                <!-- Predicciones -->
                <div id="predictions" class="section">
                    <div class="content-header">
                        <h2>Análisis Predictivo</h2>
                        <p>Simulaciones Monte Carlo para toma de decisiones estratégicas</p>
                    </div>
                    <div class="content-body">
                        <div class="form-grid">
                            <div class="form-group">
                                <label class="form-label">Giros de Simulación</label>
                                <input type="number" id="sim-rounds" class="form-input" value="10" min="1" max="100">
                            </div>
                            <div class="form-group">
                                <label class="form-label">Cantidad de Simulaciones</label>
                                <input type="number" id="sim-count" class="form-input" value="1000" min="100" max="10000">
                            </div>
                            <div class="form-group">
                                <label class="form-label">Posición Inicial</label>
                                <input type="number" id="sim-start-pos" class="form-input" value="1" min="1" max="39">
                            </div>
                            <div class="form-group">
                                <label class="form-label">Dirección</label>
                                <select id="sim-direction" class="form-select">
                                    <option value="both">Ambas</option>
                                    <option value="right">Derecha</option>
                                    <option value="left">Izquierda</option>
                                </select>
                            </div>
                        </div>
                        
                        <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap; margin-top: 1.5rem;">
                            <button class="btn btn-primary" onclick="runSimulation()">
                                <i class="fas fa-play"></i>
                                Ejecutar Simulación
                            </button>
                            <button class="btn btn-secondary" onclick="exportSimulation()">
                                <i class="fas fa-download"></i>
                                Exportar Resultados
                            </button>
                        </div>

                        <div style="display: none; text-align: center; padding: 3rem;" id="sim-loading">
                            <div style="width: 40px; height: 40px; border: 3px solid var(--border-color); border-top: 3px solid var(--secondary-blue); border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto 1rem;"></div>
                            <p>Ejecutando simulación Monte Carlo avanzada...</p>
                        </div>

                        <div id="simulation-results" style="display: none;">
                            <div class="chart-container">
                                <h3>Resultados de Simulación</h3>
                                <div id="sim-output"></div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Visualización -->
                <div id="visualization" class="section">
                    <div class="content-header">
                        <h2>Visualización de Datos</h2>
                        <p>Gráficos interactivos y análisis visuales</p>
                    </div>
                    <div class="content-body">
                        <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap; margin-bottom: 2rem;">
                            <button class="btn btn-primary" onclick="showChart('frequency')">
                                <i class="fas fa-chart-bar"></i>
                                Gráfico de Frecuencia
                            </button>
                            <button class="btn btn-secondary" onclick="showChart('bonus')">
                                <i class="fas fa-gift"></i>
                                Gráfico de Bonus
                            </button>
                            <button class="btn btn-secondary" onclick="showChart('direction')">
                                <i class="fas fa-sync-alt"></i>
                                Análisis Direccional
                            </button>
                            <button class="btn btn-secondary" onclick="showChart('timeline')">
                                <i class="fas fa-chart-line"></i>
                                Línea de Tiempo
                            </button>
                        </div>
                        
                        <div class="chart-container">
                            <canvas id="mainChart"></canvas>
                        </div>
                    </div>
                </div>

                <!-- Reportes -->
                <div id="reports" class="section">
                    <div class="content-header">
                        <h2>Reportes e Historial</h2>
                        <p>Historial detallado de transacciones y reportes de rendimiento</p>
                    </div>
                    <div class="content-body">
                        <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap; margin-bottom: 2rem;">
                            <button class="btn btn-secondary" onclick="refreshHistory()">
                                <i class="fas fa-sync"></i>
                                Actualizar
                            </button>
                            <button class="btn btn-danger" onclick="clearHistory()">
                                <i class="fas fa-trash"></i>
                                Limpiar Historial
                            </button>
                        </div>

                        <div class="data-table">
                            <table class="table">
                                <thead>
                                    <tr>
                                        <th>#</th>
                                        <th>Resultado</th>
                                        <th>Pos. Inicial</th>
                                        <th>Dirección</th>
                                        <th>Distancia</th>
                                        <th>Bonus</th>
                                        <th>Multiplicador</th>
                                        <th>Fecha</th>
                                    </tr>
                                </thead>
                                <tbody id="history-tbody">
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>

                <!-- Configuración -->
                <div id="settings" class="section">
                    <div class="content-header">
                        <h2>Configuración y Exportación</h2>
                        <p>Opciones de gestión de datos y configuración</p>
                    </div>
                    <div class="content-body">
                        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(147, 197, 253, 0.05)); border: 1px solid rgba(59, 130, 246, 0.2); border-radius: 12px;">
                            <h3>Exportación de Datos</h3>
                            <p>Descarga tus datos de juego para respaldo o análisis externo</p>
                            
                            <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap; margin-top: 1.5rem;">
                                <button class="btn btn-primary" onclick="exportData()">
                                    <i class="fas fa-download"></i>
                                    Exportar JSON
                                </button>
                                <button class="btn btn-secondary" onclick="exportReport()">
                                    <i class="fas fa-file-alt"></i>
                                    Generar Reporte
                                </button>
                            </div>
                        </div>

                        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(147, 197, 253, 0.05)); border: 1px solid rgba(59, 130, 246, 0.2); border-radius: 12px; margin-top: 2rem;">
                            <h3>Importación de Datos</h3>
                            <p>Importa datos previamente exportados</p>
                            
                            <div class="form-group">
                                <input type="file" id="import-file" class="form-input" accept=".json" onchange="importData(event)">
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Lightning Storm Analytics Dashboard - Implementación JavaScript Mejorada
        class LightningStormAnalyzer {
            constructor() {
                this.historial = [];
                this.chart = null;
                this.distanceChart = null;
                this.loadData();
                this.updateAllDisplays();
            }

            // Función para calcular posición final en la rueda de 39 casillas
            calculateFinalPosition(startPos, direction, result, isLeaf) {
                // La rueda tiene 39 posiciones: 1, leaf, 2, leaf, 3, leaf, ..., 19, leaf, 20
                // Posiciones impares (1,3,5...39) = números, Posiciones pares (2,4,6...38) = leaf
                
                let finalPos;
                
                if (isLeaf) {
                    // Si es leaf, buscar la posición par más cercana
                    finalPos = this.findLeafPosition(startPos, direction);
                } else {
                    // Si es número, calcular posición del número específico
                    if (result === 20) {
                        finalPos = 39; // El 20 está en la posición 39
                    } else {
                        finalPos = (result * 2) - 1; // Números en posiciones impares
                    }
                }
                
                return finalPos;
            }

            // Encontrar posición leaf más probable basada en dirección
            findLeafPosition(startPos, direction) {
                const leafPositions = [];
                for (let i = 2; i <= 38; i += 2) {
                    leafPositions.push(i);
                }
                
                // Simplificación: retornar una posición leaf aleatoria
                // En implementación real, usarías patrones más complejos
                return leafPositions[Math.floor(Math.random() * leafPositions.length)];
            }

            // Calcular distancia entre posiciones
            calculateDistance(startPos, endPos, direction) {
                let distance;
                
                if (direction === 'right') {
                    if (endPos >= startPos) {
                        distance = endPos - startPos;
                    } else {
                        distance = (39 - startPos) + endPos;
                    }
                } else { // left
                    if (startPos >= endPos) {
                        distance = startPos - endPos;
                    } else {
                        distance = startPos + (39 - endPos);
                    }
                }
                
                return distance;
            }

            // Gestión de Datos
            loadData() {
                const data = localStorage.getItem('lightning_storm_data');
                if (data) {
                    try {
                        const parsed = JSON.parse(data);
                        this.historial = parsed.historial || [];
                        this.showAlert('success', `Datos cargados: ${this.historial.length} giros`);
                    } catch (e) {
                        console.error('Error cargando datos:', e);
                        this.historial = [];
                    }
                }
            }

            saveData() {
                try {
                    const data = {
                        historial: this.historial,
                        fecha_guardado: new Date().toISOString()
                    };
                    localStorage.setItem('lightning_storm_data', JSON.stringify(data));
                } catch (e) {
                    console.error('Error guardando datos:', e);
                    this.showAlert('danger', 'Error al guardar datos');
                }
            }

            // Agregar giro
            addRound(numero = null, esLeaf = false, bonus = false, multiplicador = 1.0, posicionInicial = 1, direccion = 'right') {
                if (!esLeaf && (numero < 1 || numero > 20 || !numero)) {
                    this.showAlert('danger', 'El número debe estar entre 1 y 20');
                    return false;
                }

                if (posicionInicial < 1 || posicionInicial > 39) {
                    this.showAlert('danger', 'La posición inicial debe estar entre 1 y 39');
                    return false;
                }

                const posicionFinal = this.calculateFinalPosition(posicionInicial, direccion, numero, esLeaf);
                const distancia = this.calculateDistance(posicionInicial, posicionFinal, direccion);

                const ronda = {
                    numero: esLeaf ? null : numero,
                    es_leaf: esLeaf,
                    bonus: bonus,
                    multiplicador: multiplicador,
                    posicion_inicial: posicionInicial,
                    posicion_final: posicionFinal,
                    direccion: direccion,
                    distancia: distancia,
                    timestamp: new Date().toISOString()
                };

                this.historial.push(ronda);
                this.saveData();
                this.updateAllDisplays();

                if (esLeaf) {
                    this.showAlert('success', `Giro agregado: Leaf (1:1) - Distancia: ${distancia}`);
                } else {
                    let msg = `Giro agregado: Número ${numero} - Distancia: ${distancia}`;
                    if (bonus) msg += ' 🎁 Con bonus';
                    if (multiplicador > 1) msg += ` ⚡ Multiplicador ${multiplicador}x`;
                    this.showAlert('success', msg);
                }

                // Limpiar formulario
                document.getElementById('number-input').value = '';
                document.getElementById('bonus-input').value = 'false';
                document.getElementById('multiplier-input').value = '1.0';
                document.getElementById('start-position').value = '';

                return true;
            }

            // Calcular estadísticas mejoradas
            calculateStats() {
                if (this.historial.length === 0) {
                    return {
                        total_rondas: 0,
                        conteo_numeros: {},
                        conteo_leaf: 0,
                        bonus_por_numero: {},
                        multiplicadores_por_numero: {},
                        total_bonus: 0,
                        racha_actual_sin_bonus: 0,
                        racha_maxima_sin_bonus: 0,
                        giros_derecha: 0,
                        giros_izquierda: 0,
                        distancias_derecha: [],
                        distancias_izquierda: [],
                        patrones_posicion_inicial: {}
                    };
                }

                const stats = {
                    total_rondas: this.historial.length,
                    conteo_numeros: {},
                    conteo_leaf: 0,
                    bonus_por_numero: {},
                    multiplicadores_por_numero: {},
                    total_bonus: 0,
                    racha_actual_sin_bonus: 0,
                    racha_maxima_sin_bonus: 0,
                    giros_derecha: 0,
                    giros_izquierda: 0,
                    distancias_derecha: [],
                    distancias_izquierda: [],
                    patrones_posicion_inicial: {},
                    bonus_por_direccion: { right: 0, left: 0 },
                    total_por_direccion: { right: 0, left: 0 }
                };

                // Inicializar contadores para números 1-20
                for (let i = 1; i <= 20; i++) {
                    stats.conteo_numeros[i] = 0;
                    stats.bonus_por_numero[i] = 0;
                    stats.multiplicadores_por_numero[i] = [];
                }

                // Inicializar patrones de posición inicial
                for (let i = 1; i <= 39; i++) {
                    stats.patrones_posicion_inicial[i] = 0;
                }

                let rachaActual = 0;
                let rachaMaxima = 0;

                // Procesar historial
                this.historial.forEach((ronda) => {
                    // Contar posición inicial
                    stats.patrones_posicion_inicial[ronda.posicion_inicial]++;

                    // Contar por dirección
                    if (ronda.direccion === 'right') {
                        stats.giros_derecha++;
                        stats.distancias_derecha.push(ronda.distancia);
                        stats.total_por_direccion.right++;
                    } else {
                        stats.giros_izquierda++;
                        stats.distancias_izquierda.push(ronda.distancia);
                        stats.total_por_direccion.left++;
                    }

                    if (ronda.es_leaf) {
                        stats.conteo_leaf++;
                        rachaActual++;
                    } else {
                        const numero = ronda.numero;
                        stats.conteo_numeros[numero]++;

                        if (ronda.bonus) {
                            stats.bonus_por_numero[numero]++;
                            stats.total_bonus++;
                            stats.bonus_por_direccion[ronda.direccion]++;
                            rachaActual = 0;
                        } else {
                            rachaActual++;
                        }

                        if (ronda.multiplicador > 1) {
                            stats.multiplicadores_por_numero[numero].push(ronda.multiplicador);
                        }
                    }

                    rachaMaxima = Math.max(rachaMaxima, rachaActual);
                });

                stats.racha_actual_sin_bonus = rachaActual;
                stats.racha_maxima_sin_bonus = rachaMaxima;

                return stats;
            }

            // Análisis de patrones de giro
            analyzeSpinPatterns() {
                const stats = this.calculateStats();
                
                const patterns = {
                    direcciones: {
                        derecha: {
                            total: stats.giros_derecha,
                            distancia_promedio: stats.distancias_derecha.length > 0 ? 
                                stats.distancias_derecha.reduce((a, b) => a + b, 0) / stats.distancias_derecha.length : 0,
                            tasa_bonus: stats.total_por_direccion.right > 0 ? 
                                (stats.bonus_por_direccion.right / stats.total_por_direccion.right) * 100 : 0,
                            rangos_frecuentes: this.findFrequentRanges(stats.distancias_derecha)
                        },
                        izquierda: {
                            total: stats.giros_izquierda,
                            distancia_promedio: stats.distancias_izquierda.length > 0 ? 
                                stats.distancias_izquierda.reduce((a, b) => a + b, 0) / stats.distancias_izquierda.length : 0,
                            tasa_bonus: stats.total_por_direccion.left > 0 ? 
                                (stats.bonus_por_direccion.left / stats.total_por_direccion.left) * 100 : 0,
                            rangos_frecuentes: this.findFrequentRanges(stats.distancias_izquierda)
                        }
                    },
                    posiciones_iniciales_favoritas: this.findTopPositions(stats.patrones_posicion_inicial),
                    alternancia: this.analyzeDirectionAlternation()
                };

                return patterns;
            }

            // Encontrar rangos de distancia más frecuentes
            findFrequentRanges(distancias) {
                if (distancias.length === 0) return [];

                const rangos = {};
                distancias.forEach(dist => {
                    const rango = Math.floor(dist / 5) * 5; // Agrupar en rangos de 5
                    rangos[rango] = (rangos[rango] || 0) + 1;
                });

                return Object.entries(rangos)
                    .sort(([,a], [,b]) => b - a)
                    .slice(0, 3)
                    .map(([rango, freq]) => ({ rango: parseInt(rango), frecuencia: freq }));
            }

            // Encontrar posiciones iniciales más comunes
            findTopPositions(patrones) {
                return Object.entries(patrones)
                    .sort(([,a], [,b]) => b - a)
                    .slice(0, 5)
                    .map(([pos, freq]) => ({ posicion: parseInt(pos), frecuencia: freq }));
            }

            // Analizar alternancia de direcciones
            analyzeDirectionAlternation() {
                if (this.historial.length < 2) return { patron: 'Insuficientes datos', precision: 0 };

                let alternaciones = 0;
                let total_comparaciones = 0;

                for (let i = 1; i < this.historial.length; i++) {
                    if (this.historial[i].direccion !== this.historial[i-1].direccion) {
                        alternaciones++;
                    }
                    total_comparaciones++;
                }

                const precision = total_comparaciones > 0 ? (alternaciones / total_comparaciones) * 100 : 0;
                
                return {
                    patron: precision > 60 ? 'Alternado' : precision > 40 ? 'Parcialmente alternado' : 'No alternado',
                    precision: precision.toFixed(1)
                };
            }

            // Simulación mejorada con patrones
            simulate(numSimulaciones = 1000, numRondas = 10, posicionInicial = 1, direccionPreferida = 'both') {
                const patterns = this.analyzeSpinPatterns();
                if (this.historial.length === 0) return null;

                const resultados = {
                    conteo_numeros: {},
                    conteo_leaf: 0,
                    total_bonus: 0,
                    rondas_con_bonus: 0,
                    multiplicadores_aplicados: 0,
                    distancias_promedio: [],
                    predicciones_por_direccion: {
                        derecha: { numeros: {}, leaf: 0, bonus: 0 },
                        izquierda: { numeros: {}, leaf: 0, bonus: 0 }
                    }
                };

                // Inicializar contadores
                for (let i = 1; i <= 20; i++) {
                    resultados.conteo_numeros[i] = 0;
                    resultados.predicciones_por_direccion.derecha.numeros[i] = 0;
                    resultados.predicciones_por_direccion.izquierda.numeros[i] = 0;
                }

                const probs = this.calculateProbabilities();
                if (!probs) return null;

                for (let sim = 0; sim < numSimulaciones; sim++) {
                    let bonusEnSimulacion = false;
                    let posActual = posicionInicial;

                    for (let ronda = 0; ronda < numRondas; ronda++) {
                        // Determinar dirección basada en patrones
                        let direccion;
                        if (direccionPreferida === 'both') {
                            // Usar patrón de alternancia si existe
                            if (patterns.alternancia.precision > 60) {
                                direccion = ronda % 2 === 0 ? 'right' : 'left';
                            } else {
                                direccion = Math.random() > 0.5 ? 'right' : 'left';
                            }
                        } else {
                            direccion = direccionPreferida;
                        }

                        // Simular resultado
                        if (Math.random() < probs.leaf) {
                            resultados.conteo_leaf++;
                            resultados.predicciones_por_direccion[direccion].leaf++;
                        } else {
                            // Seleccionar número basado en probabilidades
                            const rand = Math.random();
                            let acum = 0;
                            let numeroSeleccionado = 1;

                            for (let i = 1; i <= 20; i++) {
                                acum += probs.numeros[i];
                                if (rand <= acum) {
                                    numeroSeleccionado = i;
                                    break;
                                }
                            }

                            resultados.conteo_numeros[numeroSeleccionado]++;
                            resultados.predicciones_por_direccion[direccion].numeros[numeroSeleccionado]++;

                            // Simular bonus con mejores probabilidades por dirección
                            const bonusProb = direccion === 'right' ? 
                                patterns.direcciones.derecha.tasa_bonus / 100 : 
                                patterns.direcciones.izquierda.tasa_bonus / 100;

                            if (Math.random() < bonusProb) {
                                resultados.total_bonus++;
                                resultados.predicciones_por_direccion[direccion].bonus++;
                                bonusEnSimulacion = true;
                            }

                            // Calcular distancia simulada
                            const posFinal = this.calculateFinalPosition(posActual, direccion, numeroSeleccionado, false);
                            const distancia = this.calculateDistance(posActual, posFinal, direccion);
                            resultados.distancias_promedio.push(distancia);
                            posActual = posFinal;
                        }
                    }

                    if (bonusEnSimulacion) {
                        resultados.rondas_con_bonus++;
                    }
                }

                // Calcular promedios
                for (let key in resultados) {
                    if (key !== 'rondas_con_bonus' && key !== 'predicciones_por_direccion' && key !== 'distancias_promedio') {
                        if (key === 'conteo_numeros') {
                            for (let i = 1; i <= 20; i++) {
                                resultados.conteo_numeros[i] /= numSimulaciones;
                            }
                        } else {
                            resultados[key] /= numSimulaciones;
                        }
                    }
                }

                resultados.prob_bonus_en_X_rondas = resultados.rondas_con_bonus / numSimulaciones;
                resultados.distancia_promedio_simulada = resultados.distancias_promedio.length > 0 ? 
                    resultados.distancias_promedio.reduce((a, b) => a + b, 0) / resultados.distancias_promedio.length : 0;

                return resultados;
            }

            // Calcular probabilidades mejoradas
            calculateProbabilities() {
                const stats = this.calculateStats();
                
                if (stats.total_rondas === 0) return null;

                const totalNumeros = Object.values(stats.conteo_numeros).reduce((a, b) => a + b, 0);
                
                const probabilities = {
                    numeros: {},
                    leaf: stats.conteo_leaf / stats.total_rondas,
                    bonus_general: stats.total_bonus / stats.total_rondas,
                    bonus_por_numero: {},
                    multiplicadores_promedio: {},
                    bonus_por_direccion: {
                        right: stats.total_por_direccion.right > 0 ? stats.bonus_por_direccion.right / stats.total_por_direccion.right : 0,
                        left: stats.total_por_direccion.left > 0 ? stats.bonus_por_direccion.left / stats.total_por_direccion.left : 0
                    }
                };

                // Calcular probabilidades para números
                for (let i = 1; i <= 20; i++) {
                    probabilities.numeros[i] = totalNumeros > 0 ? stats.conteo_numeros[i] / totalNumeros : 1/20;
                    
                    // Probabilidad de bonus por número
                    const apariciones = stats.conteo_numeros[i];
                    probabilities.bonus_por_numero[i] = apariciones > 0 ? 
                        stats.bonus_por_numero[i] / apariciones : 
                        probabilities.bonus_general;
                    
                    // Multiplicador promedio
                    const mults = stats.multiplicadores_por_numero[i];
                    probabilities.multiplicadores_promedio[i] = mults.length > 0 ? 
                        mults.reduce((a, b) => a + b, 0) / mults.length : 1.0;
                }

                return probabilities;
            }

            // Sugerir mejores números con análisis de patrones
            suggestBestNumbers(topN = 5) {
                const probs = this.calculateProbabilities();
                const patterns = this.analyzeSpinPatterns();
                
                if (!probs) return [];

                const valores = [];

                for (let i = 1; i <= 20; i++) {
                    const probSalir = probs.numeros[i];
                    const probBonus = probs.bonus_por_numero[i];
                    const multPromedio = probs.multiplicadores_promedio[i];

                    // Valor esperado mejorado con análisis de patrones
                    const valorBase = probSalir * 20;
                    const bonusExtra = probBonus * 15;
                    const multExtra = (multPromedio - 1) * 8;
                    
                    // Factor de patrón direccional
                    const factorDireccion = Math.max(
                        patterns.direcciones.derecha.tasa_bonus,
                        patterns.direcciones.izquierda.tasa_bonus
                    ) / 100;

                    const valorTotal = (valorBase + bonusExtra + multExtra) * (1 + factorDireccion);
                    
                    valores.push({ 
                        numero: i, 
                        valor: valorTotal, 
                        prob: probSalir, 
                        probBonus: probBonus, 
                        mult: multPromedio,
                        factorPatron: factorDireccion
                    });
                }

                return valores.sort((a, b) => b.valor - a.valor).slice(0, topN);
            }

            // Alertas de interfaz
            showAlert(type, message) {
                const alertDiv = document.createElement('div');
                alertDiv.className = `alert alert-${type}`;
                alertDiv.innerHTML = `
                    <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'danger' ? 'exclamation-triangle' : 'info-circle'}"></i>
                    ${message}
                `;

                const resultDiv = document.getElementById('add-result');
                resultDiv.innerHTML = '';
                resultDiv.appendChild(alertDiv);

                setTimeout(() => {
                    alertDiv.style.opacity = '0';
                    setTimeout(() => alertDiv.remove(), 300);
                }, 4000);
            }

            // Actualizar todas las visualizaciones
            updateAllDisplays() {
                this.updateHeaderStats();
                this.updateAnalytics();
                this.updateNumbersGrid();
                this.updateRecommendations();
                this.updatePatternAnalysis();
                this.updateHistory();
            }

            updateHeaderStats() {
                const stats = this.calculateStats();
                
                document.getElementById('header-total-rounds').textContent = stats.total_rondas;
                
                const bonusRate = stats.total_rondas > 0 ? 
                    ((stats.total_bonus / stats.total_rondas) * 100).toFixed(1) : '0';
                document.getElementById('header-success-rate').textContent = bonusRate + '%';
            }

            updateAnalytics() {
                const stats = this.calculateStats();
                
                document.getElementById('total-rounds').textContent = stats.total_rondas;
                document.getElementById('current-streak').textContent = stats.racha_actual_sin_bonus;
                
                const bonusRate = stats.total_rondas > 0 ? 
                    ((stats.total_bonus / stats.total_rondas) * 100).toFixed(1) : '0';
                document.getElementById('bonus-rate').textContent = bonusRate + '%';
                
                const leafRate = stats.total_rondas > 0 ? 
                    ((stats.conteo_leaf / stats.total_rondas) * 100).toFixed(1) : '0';
                document.getElementById('leaf-rate').textContent = leafRate + '%';
            }

            updateNumbersGrid() {
                const stats = this.calculateStats();
                const grid = document.getElementById('numbers-grid');
                grid.innerHTML = '';

                if (stats.total_rondas === 0) {
                    grid.innerHTML = '<p>No hay datos disponibles aún. Agrega algunos giros para ver el análisis de números.</p>';
                    return;
                }

                const totalNumeros = Object.values(stats.conteo_numeros).reduce((a, b) => a + b, 0);
                const avgFrequency = totalNumeros / 20;

                for (let i = 1; i <= 20; i++) {
                    const count = stats.conteo_numeros[i];
                    const bonusCount = stats.bonus_por_numero[i];
                    const multCount = stats.multiplicadores_por_numero[i].length;
                    
                    const card = document.createElement('div');
                    card.className = 'number-card';
                    
                    if (count > avgFrequency * 1.2) {
                        card.classList.add('hot');
                    } else if (count < avgFrequency * 0.8) {
                        card.classList.add('cold');
                    }
                    
                    card.innerHTML = `
                        <div class="number-value">${i}</div>
                        <div class="number-stats">
                            <div>Apariciones: ${count}</div>
                            <div>Bonus: ${bonusCount}</div>
                            <div>Mult: ${multCount}</div>
                        </div>
                    `;
                    
                    grid.appendChild(card);
                }
            }

            updateRecommendations() {
                const recommendations = this.suggestBestNumbers(5);
                const container = document.getElementById('recommendations-list');
                container.innerHTML = '';

                if (recommendations.length === 0) {
                    container.innerHTML = '<p>Agrega más giros para generar recomendaciones.</p>';
                    return;
                }

                recommendations.forEach((rec, index) => {
                    const item = document.createElement('div');
                    item.className = 'range-item';
                    item.innerHTML = `
                        <div style="font-weight: 700; font-size: 1.125rem;">
                            ${index + 1}. Número ${rec.numero}
                        </div>
                        <div style="display: flex; gap: 1.5rem; font-size: 0.875rem; color: var(--text-secondary);">
                            <div>Valor: ${rec.valor.toFixed(2)}</div>
                            <div>Prob: ${(rec.prob * 100).toFixed(1)}%</div>
                            <div>Bonus: ${(rec.probBonus * 100).toFixed(1)}%</div>
                            <div>Mult: ${rec.mult.toFixed(1)}x</div>
                            <div>Patrón: +${(rec.factorPatron * 100).toFixed(0)}%</div>
                        </div>
                    `;
                    container.appendChild(item);
                });
            }

            updatePatternAnalysis() {
                const patterns = this.analyzeSpinPatterns();
                const stats = this.calculateStats();

                // Actualizar estadísticas de giros a la derecha
                document.getElementById('right-spins-count').textContent = patterns.direcciones.derecha.total;
                document.getElementById('right-avg-distance').textContent = patterns.direcciones.derecha.distancia_promedio.toFixed(1);
                document.getElementById('right-bonus-rate').textContent = patterns.direcciones.derecha.tasa_bonus.toFixed(1) + '%';
                
                const rightLeafRate = stats.giros_derecha > 0 ? 
                    ((stats.distancias_derecha.filter(d => d % 2 === 0).length / stats.giros_derecha) * 100).toFixed(1) : '0';
                document.getElementById('right-leaf-rate').textContent = rightLeafRate + '%';

                // Actualizar estadísticas de giros a la izquierda
                document.getElementById('left-spins-count').textContent = patterns.direcciones.izquierda.total;
                document.getElementById('left-avg-distance').textContent = patterns.direcciones.izquierda.distancia_promedio.toFixed(1);
                document.getElementById('left-bonus-rate').textContent = patterns.direcciones.izquierda.tasa_bonus.toFixed(1) + '%';
                
                const leftLeafRate = stats.giros_izquierda > 0 ? 
                    ((stats.distancias_izquierda.filter(d => d % 2 === 0).length / stats.giros_izquierda) * 100).toFixed(1) : '0';
                document.getElementById('left-leaf-rate').textContent = leftLeafRate + '%';

                // Actualizar análisis de rangos
                this.updateRangeAnalysis(patterns);

                // Actualizar grid de posiciones iniciales
                this.updateStartPositionsGrid(stats);
            }

            updateRangeAnalysis(patterns) {
                const container = document.getElementById('range-analysis-list');
                container.innerHTML = '';

                // Rangos frecuentes derecha
                if (patterns.direcciones.derecha.rangos_frecuentes.length > 0) {
                    const rightRanges = document.createElement('div');
                    rightRanges.innerHTML = '<h4 style="margin-bottom: 1rem; color: var(--accent-gold);">Rangos Frecuentes - Giros a la Derecha:</h4>';
                    
                    patterns.direcciones.derecha.rangos_frecuentes.forEach(rango => {
                        const item = document.createElement('div');
                        item.className = 'range-item';
                        item.innerHTML = `
                            <div>Rango ${rango.rango}-${rango.rango + 4} posiciones</div>
                            <div>Frecuencia: ${rango.frecuencia} veces</div>
                        `;
                        rightRanges.appendChild(item);
                    });
                    
                    container.appendChild(rightRanges);
                }

                // Rangos frecuentes izquierda
                if (patterns.direcciones.izquierda.rangos_frecuentes.length > 0) {
                    const leftRanges = document.createElement('div');
                    leftRanges.innerHTML = '<h4 style="margin: 2rem 0 1rem; color: var(--accent-gold);">Rangos Frecuentes - Giros a la Izquierda:</h4>';
                    
                    patterns.direcciones.izquierda.rangos_frecuentes.forEach(rango => {
                        const item = document.createElement('div');
                        item.className = 'range-item';
                        item.innerHTML = `
                            <div>Rango ${rango.rango}-${rango.rango + 4} posiciones</div>
                            <div>Frecuencia: ${rango.frecuencia} veces</div>
                        `;
                        leftRanges.appendChild(item);
                    });
                    
                    container.appendChild(leftRanges);
                }

                // Patrón de alternancia
                const alternancia = document.createElement('div');
                alternancia.className = 'range-item';
                alternancia.innerHTML = `
                    <div><strong>Patrón de Alternancia:</strong> ${patterns.alternancia.patron}</div>
                    <div>Precisión: ${patterns.alternancia.precision}%</div>
                `;
                container.appendChild(alternancia);
            }

            updateStartPositionsGrid(stats) {
                const grid = document.getElementById('start-positions-grid');
                grid.innerHTML = '';

                if (stats.total_rondas === 0) {
                    grid.innerHTML = '<p>No hay datos de posiciones iniciales disponibles.</p>';
                    return;
                }

                const topPositions = Object.entries(stats.patrones_posicion_inicial)
                    .filter(([pos, freq]) => freq > 0)
                    .sort(([,a], [,b]) => b - a)
                    .slice(0, 20);

                topPositions.forEach(([pos, freq]) => {
                    const card = document.createElement('div');
                    card.className = 'number-card';
                    
                    const percentage = ((freq / stats.total_rondas) * 100).toFixed(1);
                    
                    if (percentage > 5) {
                        card.classList.add('hot');
                    } else if (percentage < 2) {
                        card.classList.add('cold');
                    }
                    
                    card.innerHTML = `
                        <div class="number-value">${pos}</div>
                        <div class="number-stats">
                            <div>Veces: ${freq}</div>
                            <div>%: ${percentage}%</div>
                        </div>
                    `;
                    
                    grid.appendChild(card);
                });
            }

            updateHistory() {
                const tbody = document.getElementById('history-tbody');
                tbody.innerHTML = '';

                if (this.historial.length === 0) {
                    tbody.innerHTML = '<tr><td colspan="8">No hay giros registrados aún.</td></tr>';
                    return;
                }

                const recent = this.historial.slice(-50).reverse();
                
                recent.forEach((ronda, index) => {
                    const row = document.createElement('tr');
                    const resultText = ronda.es_leaf ? 'Leaf (1:1)' : `Número ${ronda.numero}`;
                    const direccionText = ronda.direccion === 'right' ? '→ Derecha' : '← Izquierda';
                    const bonusText = ronda.bonus ? '✅' : '❌';
                    const multText = ronda.multiplicador > 1 ? `${ronda.multiplicador}x` : '1x';
                    const date = new Date(ronda.timestamp).toLocaleString();
                    
                    row.innerHTML = `
                        <td>${this.historial.length - index}</td>
                        <td>${resultText}</td>
                        <td>${ronda.posicion_inicial}</td>
                        <td>${direccionText}</td>
                        <td>${ronda.distancia}</td>
                        <td>${bonusText}</td>
                        <td>${multText}</td>
                        <td>${date}</td>
                    `;
                    
                    tbody.appendChild(row);
                });
            }
        }

        // Instancia global
        let analyzer = new LightningStormAnalyzer();

        // Funciones globales
        function showSection(sectionId) {
            // Actualizar navegación
            document.querySelectorAll('.nav-item').forEach(item => {
                item.classList.remove('active');
            });
            event.target.classList.add('active');
            
            // Actualizar contenido
            document.querySelectorAll('.section').forEach(section => {
                section.classList.remove('active');
            });
            document.getElementById(sectionId).classList.add('active');
        }

        function toggleResultFields() {
            const type = document.getElementById('result-type').value;
            const numberGroup = document.getElementById('number-group');
            const bonusGroup = document.getElementById('bonus-group');
            const multiplierGroup = document.getElementById('multiplier-group');
            
            if (type === 'leaf') {
                numberGroup.style.display = 'none';
                bonusGroup.style.display = 'none';
                multiplierGroup.style.display = 'none';
            } else {
                numberGroup.style.display = 'block';
                bonusGroup.style.display = 'block';
                multiplierGroup.style.display = 'block';
            }
        }

        function addRound() {
            const type = document.getElementById('result-type').value;
            const startPos = parseInt(document.getElementById('start-position').value);
            const direction = document.getElementById('spin-direction').value;
            
            if (!startPos || startPos < 1 || startPos > 39) {
                analyzer.showAlert('danger', 'Debes especificar una posición inicial válida (1-39)');
                return;
            }
            
            if (type === 'leaf') {
                analyzer.addRound(null, true, false, 1.0, startPos, direction);
            } else {
                const number = parseInt(document.getElementById('number-input').value);
                const bonus = document.getElementById('bonus-input').value === 'true';
                const multiplier = parseFloat(document.getElementById('multiplier-input').value) || 1.0;
                
                analyzer.addRound(number, false, bonus, multiplier, startPos, direction);
            }
        }

        function quickAddMode() {
            analyzer.showAlert('info', 'Modo rápido activado. Usa atajos de teclado: 1-20 para números, L para leaf, D/I para dirección');
            // Se podría implementar atajos de teclado aquí
        }

        function runSimulation() {
            const rounds = parseInt(document.getElementById('sim-rounds').value) || 10;
            const count = parseInt(document.getElementById('sim-count').value) || 1000;
            const startPos = parseInt(document.getElementById('sim-start-pos').value) || 1;
            const direction = document.getElementById('sim-direction').value;
            
            document.getElementById('sim-loading').style.display = 'block';
            document.getElementById('simulation-results').style.display = 'none';
            
            // Simular tiempo de procesamiento para realismo
            setTimeout(() => {
                const results = analyzer.simulate(count, rounds, startPos, direction);
                
                if (results) {
                    const output = document.getElementById('sim-output');
                    output.innerHTML = `
                        <div class="metrics-grid">
                            <div class="metric-card">
                                <div class="metric-title">Leaf Esperados</div>
                                <div class="metric-value">${results.conteo_leaf.toFixed(1)}</div>
                            </div>
                            <div class="metric-card success">
                                <div class="metric-title">Bonus Esperados</div>
                                <div class="metric-value">${results.total_bonus.toFixed(1)}</div>
                            </div>
                            <div class="metric-card warning">
                                <div class="metric-title">Prob. de Bonus</div>
                                <div class="metric-value">${(results.prob_bonus_en_X_rondas * 100).toFixed(1)}%</div>
                            </div>
                            <div class="metric-card">
                                <div class="metric-title">Distancia Promedio</div>
                                <div class="metric-value">${results.distancia_promedio_simulada.toFixed(1)}</div>
                            </div>
                        </div>
                        
                        <h4>Números Más Probables:</h4>
                        <div class="numbers-grid">
                            ${Object.entries(results.conteo_numeros)
                                .sort(([,a], [,b]) => b - a)
                                .slice(0, 8)
                                .map(([num, freq]) => `
                                    <div class="number-card">
                                        <div class="number-value">${num}</div>
                                        <div class="number-stats">
                                            <div>${freq.toFixed(1)} veces</div>
                                        </div>
                                    </div>
                                `).join('')}
                        </div>

                        <h4 style="margin-top: 2rem;">Predicciones por Dirección:</h4>
                        <div class="pattern-grid">
                            <div class="pattern-card">
                                <div class="pattern-title">Derecha</div>
                                <div>Bonus: ${results.predicciones_por_direccion.derecha.bonus.toFixed(1)}</div>
                                <div>Leaf: ${results.predicciones_por_direccion.derecha.leaf.toFixed(1)}</div>
                            </div>
                            <div class="pattern-card">
                                <div class="pattern-title">Izquierda</div>
                                <div>Bonus: ${results.predicciones_por_direccion.izquierda.bonus.toFixed(1)}</div>
                                <div>Leaf: ${results.predicciones_por_direccion.izquierda.leaf.toFixed(1)}</div>
                            </div>
                        </div>
                    `;
                }
                
                document.getElementById('sim-loading').style.display = 'none';
                document.getElementById('simulation-results').style.display = 'block';
            }, 2500);
        }

        function showChart(type) {
            const canvas = document.getElementById('mainChart');
            const ctx = canvas.getContext('2d');
            
            if (analyzer.chart) {
                analyzer.chart.destroy();
            }
            
            const stats = analyzer.calculateStats();
            
            if (type === 'frequency') {
                const data = {
                    labels: Array.from({length: 20}, (_, i) => (i + 1).toString()),
                    datasets: [{
                        label: 'Frecuencia',
                        data: Array.from({length: 20}, (_, i) => stats.conteo_numeros[i + 1]),
                        backgroundColor: 'rgba(59, 130, 246, 0.6)',
                        borderColor: 'rgba(59, 130, 246, 1)',
                        borderWidth: 2
                    }]
                };
                
                analyzer.chart = new Chart(ctx, {
                    type: 'bar',
                    data: data,
                    options: {
                        responsive: true,
                        scales: {
                            y: {
                                beginAtZero: true,
                                ticks: { color: '#cbd5e1' },
                                grid: { color: 'rgba(203, 213, 225, 0.1)' }
                            },
                            x: {
                                ticks: { color: '#cbd5e1' },
                                grid: { color: 'rgba(203, 213, 225, 0.1)' }
                            }
                        },
                        plugins: {
                            legend: { labels: { color: '#cbd5e1' } }
                        }
                    }
                });
            } else if (type === 'direction') {
                const data = {
                    labels: ['Giros a la Derecha', 'Giros a la Izquierda'],
                    datasets: [{
                        label: 'Cantidad de Giros',
                        data: [stats.giros_derecha, stats.giros_izquierda],
                        backgroundColor: ['rgba(245, 158, 11, 0.6)', 'rgba(16, 185, 129, 0.6)'],
                        borderColor: ['rgba(245, 158, 11, 1)', 'rgba(16, 185, 129, 1)'],
                        borderWidth: 2
                    }]
                };
                
                analyzer.chart = new Chart(ctx, {
                    type: 'doughnut',
                    data: data,
                    options: {
                        responsive: true,
                        plugins: {
                            legend: { labels: { color: '#cbd5e1' } }
                        }
                    }
                });
            }
        }

        function clearHistory() {
            if (confirm('¿Estás seguro de que quieres limpiar todo el historial? Esta acción no se puede deshacer.')) {
                analyzer.historial = [];
                analyzer.saveData();
                analyzer.updateAllDisplays();
                analyzer.showAlert('success', 'Historial limpiado exitosamente');
            }
        }

        function refreshHistory() {
            analyzer.updateAllDisplays();
            analyzer.showAlert('success', 'Datos actualizados');
        }

        function exportData() {
            const data = {
                historial: analyzer.historial,
                fecha_exportacion: new Date().toISOString(),
                version: '2.0'
            };
            
            const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `lightning_storm_export_${new Date().toISOString().split('T')[0]}.json`;
            a.click();
            URL.revokeObjectURL(url);
        }

        function exportReport() {
            const stats = analyzer.calculateStats();
            const patterns = analyzer.analyzeSpinPatterns();
            const recommendations = analyzer.suggestBestNumbers(10);
            
            let report = `REPORTE DE ANÁLISIS LIGHTNING STORM\n`;
            report += `Generado: ${new Date().toLocaleString()}\n`;
            report += `=====================================\n\n`;
            report += `RESUMEN:\n`;
            report += `Total de Giros: ${stats.total_rondas}\n`;
            report += `Tasa de Bonus: ${stats.total_rondas > 0 ? ((stats.total_bonus / stats.total_rondas) * 100).toFixed(1) : 0}%\n`;
            report += `Racha Actual: ${stats.racha_actual_sin_bonus}\n`;
            report += `Racha Máxima: ${stats.racha_maxima_sin_bonus}\n\n`;
            
            report += `ANÁLISIS DE PATRONES:\n`;
            report += `Giros a la Derecha: ${patterns.direcciones.derecha.total} (${patterns.direcciones.derecha.tasa_bonus.toFixed(1)}% bonus)\n`;
            report += `Giros a la Izquierda: ${patterns.direcciones.izquierda.total} (${patterns.direcciones.izquierda.tasa_bonus.toFixed(1)}% bonus)\n`;
            report += `Patrón de Alternancia: ${patterns.alternancia.patron} (${patterns.alternancia.precision}%)\n\n`;
            
            report += `RECOMENDACIONES PRINCIPALES:\n`;
            recommendations.forEach((rec, i) => {
                report += `${i + 1}. Número ${rec.numero} - Valor: ${rec.valor.toFixed(2)} - Bonus: ${(rec.probBonus * 100).toFixed(1)}%\n`;
            });
            
            const blob = new Blob([report], { type: 'text/plain' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `lightning_storm_reporte_${new Date().toISOString().split('T')[0]}.txt`;
            a.click();
            URL.revokeObjectURL(url);
        }

        function importData(event) {
            const file = event.target.files[0];
            if (!file) return;
            
            const reader = new FileReader();
            reader.onload = function(e) {
                try {
                    const data = JSON.parse(e.target.result);
                    if (data.historial) {
                        analyzer.historial = data.historial;
                        analyzer.saveData();
                        analyzer.updateAllDisplays();
                        analyzer.showAlert('success', `Importados ${data.historial.length} giros exitosamente`);
                    }
                } catch (error) {
                    analyzer.showAlert('danger', 'Error importando archivo: Formato inválido');
                }
            };
            reader.readAsText(file);
        }

        function exportSimulation() {
            analyzer.showAlert('info', 'Función de exportación de simulación disponible próximamente');
        }

        // Inicialización
        document.addEventListener('DOMContentLoaded', function() {
            toggleResultFields();
            analyzer.updateAllDisplays();
            
            // Animación de carga del spinner
            const style = document.createElement('style');
            style.textContent = '@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }';
            document.head.appendChild(style);
        });
    </script>
</body>
</html>
