from django.http import HttpResponse
from django.shortcuts import render

# Lista de personal enriquecida con información corporativa
personal = [
    {"nombre": "fiorella", "cargo": "Directora de Operaciones", "dpto": "Gerencia", "email": "f.alvarez@empresa.com", "estado": "Activo"},
    {"nombre": "camila", "cargo": "Lead UX/UI Designer", "dpto": "Diseño", "email": "c.rodriguez@empresa.com", "estado": "Activo"},
    {"nombre": "vanesa", "cargo": "Senior Backend Developer", "dpto": "Tecnología", "email": "v.mendoza@empresa.com", "estado": "En Reunión"},
    {"nombre": "sofia", "cargo": "Analista de Datos", "dpto": "Tecnología", "email": "s.gomez@empresa.com", "estado": "Activo"},
    {"nombre": "mateo", "cargo": "DevOps Engineer", "dpto": "Tecnología", "email": "m.silva@empresa.com", "estado": "Ausente"},
    {"nombre": "lucia", "cargo": "Especialista HR", "dpto": "Recursos Humanos", "email": "l.torres@empresa.com", "estado": "Activo"},
    {"nombre": "diego", "cargo": "Consultor Financiero", "dpto": "Finanzas", "email": "d.morales@empresa.com", "estado": "Activo"},
    {"nombre": "valentina", "cargo": "Social Media Manager", "dpto": "Marketing", "email": "v.perez@empresa.com", "estado": "En Reunión"},
]

def listar(request):
    filas_html = ""
    for i, p in enumerate(personal, start=1):
        nombre_fmt = p["nombre"].capitalize()
        inicial = p["nombre"][0].upper()
        
        # Color del badge de estado según la actividad
        if p["estado"] == "Activo":
            badge_class = "badge-active"
            dot_class = "dot-green"
        elif p["estado"] == "En Reunión":
            badge_class = "badge-busy"
            dot_class = "dot-amber"
        else:
            badge_class = "badge-away"
            dot_class = "dot-gray"

        filas_html += f"""
        <tr>
            <td class="id-col">#EMP-0{i:02d}</td>
            <td>
                <div class="user-cell">
                    <div class="avatar">{inicial}</div>
                    <div class="user-info">
                        <span class="name">{nombre_fmt}</span>
                        <span class="email">{p['email']}</span>
                    </div>
                </div>
            </td>
            <td>
                <div class="role-info">
                    <span class="role">{p['cargo']}</span>
                    <span class="dept">{p['dpto']}</span>
                </div>
            </td>
            <td>
                <span class="badge {badge_class}">
                    <span class="dot {dot_class}"></span> {p['estado']}
                </span>
            </td>
            <td class="text-right">
                <button class="btn-action" title="Opciones">⋮</button>
            </td>
        </tr>
        """

    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Control de Personal - Dashboard</title>
        <style>
            * {{
                box-sizing: border-box;
                margin: 0;
                padding: 0;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            }}
            body {{
                background-color: #0b0f19; /* Oscuro profundo */
                color: #e2e8f0;
                padding: 30px 15px;
                display: flex;
                justify-content: center;
            }}
            .dashboard {{
                width: 100%;
                max-width: 950px;
                background-color: #151c2c;
                border: 1px solid #283548;
                border-radius: 12px;
                box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
                overflow: hidden;
            }}
            /* Header corporativo con acciones */
            .header {{
                padding: 24px;
                background-color: #1b2438;
                border-bottom: 1px solid #283548;
                display: flex;
                justify-content: space-between;
                align-items: center;
                flex-wrap: wrap;
                gap: 16px;
            }}
            .header-title h1 {{
                font-size: 1.25rem;
                font-weight: 700;
                color: #f8fafc;
                letter-spacing: -0.02em;
            }}
            .header-title p {{
                font-size: 0.85rem;
                color: #8b9bb4;
                margin-top: 2px;
            }}
            .header-stats {{
                display: flex;
                gap: 12px;
            }}
            .stat-chip {{
                background-color: #0b0f19;
                border: 1px solid #283548;
                padding: 6px 14px;
                border-radius: 20px;
                font-size: 0.75rem;
                color: #94a3b8;
            }}
            .stat-chip strong {{
                color: #38bdf8;
            }}
            /* Tabla estilo Enterprise */
            table {{
                width: 100%;
                border-collapse: collapse;
                text-align: left;
                font-size: 0.875rem;
            }}
            th {{
                background-color: #0f172a;
                padding: 14px 24px;
                font-weight: 600;
                color: #64748b;
                text-transform: uppercase;
                font-size: 0.7rem;
                letter-spacing: 0.08em;
                border-bottom: 1px solid #283548;
            }}
            td {{
                padding: 16px 24px;
                border-bottom: 1px solid #1e293b;
                vertical-align: middle;
            }}
            tr:hover {{
                background-color: #1e293b;
            }}
            .id-col {{
                color: #64748b;
                font-family: monospace;
                font-size: 0.75rem;
                width: 100px;
            }}
            /* Avatar + Info Usuario */
            .user-cell {{
                display: flex;
                align-items: center;
                gap: 12px;
            }}
            .avatar {{
                width: 38px;
                height: 38px;
                border-radius: 8px;
                background: linear-gradient(135deg, #1e3a8a, #3b82f6);
                color: #ffffff;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: 700;
                font-size: 0.9rem;
                box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            }}
            .user-info {{
                display: flex;
                flex-direction: column;
            }}
            .name {{
                font-weight: 600;
                color: #f1f5f9;
                font-size: 0.9rem;
            }}
            .email {{
                font-size: 0.75rem;
                color: #64748b;
            }}
            /* Cargo y Departamento */
            .role-info {{
                display: flex;
                flex-direction: column;
            }}
            .role {{
                color: #cbd5e1;
                font-weight: 500;
            }}
            .dept {{
                font-size: 0.75rem;
                color: #64748b;
            }}
            /* Badges de estado */
            .badge {{
                display: inline-flex;
                align-items: center;
                gap: 6px;
                padding: 4px 10px;
                border-radius: 6px;
                font-size: 0.75rem;
                font-weight: 500;
            }}
            .badge-active {{ background-color: rgba(6, 78, 59, 0.4); color: #6ee7b7; border: 1px solid #047857; }}
            .badge-busy {{ background-color: rgba(120, 53, 15, 0.4); color: #fcd34d; border: 1px solid #b45309; }}
            .badge-away {{ background-color: rgba(30, 41, 59, 0.6); color: #94a3b8; border: 1px solid #475569; }}
            .dot {{ width: 6px; height: 6px; border-radius: 50%; }}
            .dot-green {{ background-color: #10b981; }}
            .dot-amber {{ background-color: #f59e0b; }}
            .dot-gray {{ background-color: #64748b; }}
            
            /* Botón de acción */
            .btn-action {{
                background: none;
                border: none;
                color: #64748b;
                font-size: 1.2rem;
                cursor: pointer;
                padding: 4px 8px;
                border-radius: 4px;
            }}
            .btn-action:hover {{
                color: #f8fafc;
                background-color: #283548;
            }}
            .text-right {{ text-align: right; }}

            /* Footer */
            .footer {{
                padding: 14px 24px;
                background-color: #0f172a;
                border-top: 1px solid #283548;
                font-size: 0.75rem;
                color: #64748b;
                display: flex;
                justify-content: space-between;
            }}
        </style>
    </head>
    <body>
        <div class="dashboard">
            <div class="header">
                <div class="header-title">
                    <h1>Directorio Ejecutivo de Personal</h1>
                    <p>Gestión centralizada de cuentas e integrantes del equipo</p>
                </div>
                <div class="header-stats">
                    <span class="stat-chip">Total: <strong>{len(personal)}</strong></span>
                    <span class="stat-chip">Sede: <strong>Central</strong></span>
                </div>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Código</th>
                        <th>Empleado</th>
                        <th>Puesto / Área</th>
                        <th>Estado</th>
                        <th class="text-right">Acción</th>
                    </tr>
                </thead>
                <tbody>
                    {filas_html}
                </tbody>
            </table>
            <div class="footer">
                <span>Enterprise Suite v2.4</span>
                <span>Última sincronización: Hoy</span>
            </div>
        </div>
    </body>
    </html>
    """
    
    return HttpResponse(html_content)
def saludar(request):
    texto = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Curso de Python con Django</title>
        <style>
            * {
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }
            body {
                font-family: 'Inter', system-ui, -apple-system, sans-serif;
                background-color: #0f172a;
                color: #f8fafc;
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }
            .card {
                background: rgba(30, 41, 59, 0.7);
                backdrop-filter: blur(12px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 24px;
                padding: 40px;
                max-width: 500px;
                width: 100%;
                box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
                text-align: left;
            }
            .badge {
                display: inline-block;
                background-color: #059669;
                color: #ecfdf5;
                font-size: 0.8rem;
                font-weight: 600;
                padding: 4px 12px;
                border-radius: 9999px;
                margin-bottom: 16px;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }
            h1 {
                font-size: 2rem;
                font-weight: 800;
                line-height: 1.2;
                margin-bottom: 12px;
            }
            .highlight {
                color: #f59e0b;
            }
            p {
                color: #94a3b8;
                font-size: 1rem;
                margin-bottom: 24px;
                line-height: 1.5;
            }
            .btn {
                display: inline-block;
                background-color: #0f766e;
                color: #ffffff;
                text-decoration: none;
                font-weight: 600;
                padding: 12px 24px;
                border-radius: 12px;
                transition: all 0.2s ease;
                box-shadow: 0 4px 6px -1px rgba(15, 118, 110, 0.4);
            }
            .btn:hover {
                background-color: #115e59;
                transform: translateY(-2px);
            }
        </style>
    </head>
    <body>
        <div class="card">
            <span class="badge">Nivel 1: Primeros pasos</span>
            <h1>¡Hola! Bienvenidos al curso <span class="highlight">Python con Django</span></h1>
            <p>Aprende el desarrollo web moderno y crea aplicaciones sólidas desde cero.</p>
            <a href="#" class="btn">Empezar lección 1</a>
        </div>
    </body>
    </html>
    """
    return HttpResponse(texto)

def saludar_nombre(request, nombre):
    texto = f"Hola {nombre}"
    return HttpResponse(texto)

def factorial(request, numero):
    resultado = 1
    for i in range(1, numero + 1):
        resultado = resultado * i

        return HttpResponse(f"El factorial de {numero} es {resultado}")


def inicio_render(request):
    return render(request, 'app1/inicio.html')