
# ── Triggers ──────────────────────────────────────────────────────────────────

TRIGGERS_MENU_PRINCIPAL: frozenset[str] = frozenset({
    "hola", "menu", "menú", "inicio", "start",
    "ayuda", "help", "opciones", "hi", "hello",
    "menu_principal",          # button_reply del follow-up
    "0",                       # comando rápido
})

TRIGGERS_ESTADO_ACADEMICO: frozenset[str] = frozenset({
    "estado", "consultar", "estado_academico",
})

# ── Follow-up y encuesta ──────────────────────────────────────────────────────

FOLLOW_UP: dict = {
    "type": "buttons",
    "body": "¿Deseas realizar otra consulta? 😊",
    "buttons": [
        {"id": "menu_principal", "title": "🏠 Menú principal"},
        {"id": "hablar_asesor",  "title": "👤 Hablar con asesor"},
        {"id": "finalizar",      "title": "❌ Finalizar"},
    ],
}

ENCUESTA: dict = {
    "type": "buttons",
    "body": (
        "⭐ *Encuesta de satisfacción*\n\n"
        "¿Cómo calificarías la atención recibida hoy?\n\n"
        "Tu opinión nos ayuda a mejorar. 🙏"
    ),
    "buttons": [
        {"id": "enc_excelente", "title": "⭐⭐⭐⭐⭐ Excelente"},
        {"id": "enc_regular",   "title": "⭐⭐⭐ Regular"},
        {"id": "enc_malo",      "title": "👎 Malo"},
    ],
}

ENCUESTA_RESPUESTAS: dict[str, str] = {
    "enc_excelente": (
        "⭐⭐⭐⭐⭐ *¡Muchas gracias!*\n\n"
        "Tu opinión nos motiva a seguir mejorando cada día. 💪\n\n"
        "Fue un placer atenderte. Escribe *hola* cuando necesites ayuda. 👋"
    ),
    "enc_regular": (
        "⭐⭐⭐ *Gracias por tu honestidad.*\n\n"
        "Trabajamos continuamente para brindarte una mejor experiencia.\n\n"
        "Escribe *hola* cuando necesites ayuda. 👋"
    ),
    "enc_malo": (
        "👎 *Lamentamos tu experiencia.*\n\n"
        "Tu caso será revisado por nuestro equipo de calidad.\n"
        "📞 Si necesitas atención urgente: (601) 123-4567\n\n"
        "Escribe *hola* cuando necesites ayuda. 👋"
    ),
}

# ── Menú principal ────────────────────────────────────────────────────────────

MAIN_MENU: dict = {
    "type": "list",
    "body": (
        "👋 ¡Hola! Soy *Sally*, tu asistente universitaria.\n\n"
        "Estoy aquí para ayudarte con lo que necesites. 😊\n"
        "Selecciona una opción del menú:"
    ),
    "button_text": "📋 Ver servicios",
    "sections": [
        {
            "title": "📚 Servicios Académicos",
            "rows": [
                {
                    "id":          "matriculas",
                    "title":       "🎓 Matrículas",
                    "description": "Fechas, costos y requisitos",
                },
                {
                    "id":          "certificados",
                    "title":       "📄 Certificados",
                    "description": "Solicitar documentos oficiales",
                },
                {
                    "id":          "horarios",
                    "title":       "📅 Horarios",
                    "description": "Consultar horario de clases",
                },
            ],
        },
        {
            "title": "🛠️ Soporte y Gestión",
            "rows": [
                {
                    "id":          "soporte",
                    "title":       "🛠️ Soporte Técnico",
                    "description": "Problemas con sistemas y acceso",
                },
                {
                    "id":          "pqrs",
                    "title":       "📝 PQRS",
                    "description": "Peticiones, quejas y reclamos",
                },
                {
                    "id":          "estado_academico",
                    "title":       "🎓 Estado Académico",
                    "description": "Consultar tu información personal",
                },
            ],
        },
    ],
}

# ── Submenús ──────────────────────────────────────────────────────────────────

SUBMENUS: dict[str, dict] = {

    "matriculas": {
        "type":        "list",
        "body":        "🎓 *Matrículas*\n\nSelecciona la información que necesitas:",
        "button_text": "Ver opciones",
        "sections": [
            {
                "title": "Información de Matrícula",
                "rows": [
                    {
                        "id":          "mat_fechas",
                        "title":       "📅 Fechas de matrícula",
                        "description": "Períodos de inscripción vigentes",
                    },
                    {
                        "id":          "mat_costos",
                        "title":       "💰 Costos por crédito",
                        "description": "Valores según estrato",
                    },
                    {
                        "id":          "mat_requisitos",
                        "title":       "📋 Requisitos",
                        "description": "Documentos y condiciones",
                    },
                    {
                        "id":          "mat_asesor",
                        "title":       "👤 Hablar con asesor",
                        "description": "Atención personalizada de matrículas",
                    },
                ],
            }
        ],
    },

    "certificados": {
        "type": "buttons",
        "body": "📄 *Certificados*\n\n¿Qué tipo de certificado necesitas?",
        "buttons": [
            {"id": "cert_academico",  "title": "🎓 Cert. académico"},
            {"id": "cert_notas",      "title": "📊 Cert. de notas"},
            {"id": "cert_matricula",  "title": "📋 Cert. matrícula"},
        ],
    },

    "soporte": {
        "type": "buttons",
        "body": "🛠️ *Soporte Técnico*\n\n¿Con qué necesitas ayuda?",
        "buttons": [
            {"id": "sop_contrasena", "title": "🔑 Olvidé clave"},
            {"id": "sop_acceso",     "title": "🚫 Sin acceso"},
            {"id": "sop_ticket",     "title": "🎫 Abrir ticket"},
        ],
    },

    "pqrs": {
        "type":        "list",
        "body":        "📝 *PQRS*\n\n¿Qué tipo de solicitud deseas realizar?",
        "button_text": "Seleccionar",
        "sections": [
            {
                "title": "Tipo de solicitud",
                "rows": [
                    {
                        "id":          "pqrs_peticion",
                        "title":       "📌 Petición",
                        "description": "Solicitud de información o acción",
                    },
                    {
                        "id":          "pqrs_queja",
                        "title":       "😤 Queja",
                        "description": "Inconformidad con un servicio",
                    },
                    {
                        "id":          "pqrs_reclamo",
                        "title":       "⚠️ Reclamo",
                        "description": "Exigir reconocimiento de un derecho",
                    },
                    {
                        "id":          "pqrs_sugerencia",
                        "title":       "💡 Sugerencia",
                        "description": "Proponer mejoras al servicio",
                    },
                ],
            }
        ],
    },

    "horarios": {
        "type": "buttons",
        "body": "📅 *Horarios*\n\n¿Qué deseas hacer?",
        "buttons": [
            {"id": "hor_consultar", "title": "🔍 Consultar horario"},
            {"id": "hor_descargar", "title": "📥 Descargar horario"},
            {"id": "hor_problema",  "title": "⚠️ Reportar problema"},
        ],
    },
}

# ── Contenido de respuestas específicas ───────────────────────────────────────

CONTENT: dict[str, str] = {

    # ── MATRÍCULAS ────────────────────────────────────────────────────────────
    "mat_fechas": (
        "📅 *Fechas de Matrícula 2025*\n\n"
        "🗓️ *Período 2025-1:* 15 Ene - 31 Ene\n"
        "🗓️ *Período 2025-2:* 15 Jun - 31 Jun\n\n"
        "⚠️ *Matrícula extemporánea:* primeros 5 días hábiles del período.\n\n"
        "📌 Realiza tu inscripción en:\n"
        "*portal.universidad.edu > Matrículas*"
    ),
    "mat_costos": (
        "💰 *Costos por Crédito Académico*\n\n"
        "📊 Según clasificación socioeconómica:\n\n"
        "• Estrato 1-2: $120,000 por crédito\n"
        "• Estrato 3-4: $180,000 por crédito\n"
        "• Estrato 5-6: $250,000 por crédito\n\n"
        "💳 *Métodos de pago:* PSE, efectivo, tarjeta débito/crédito.\n"
        "🏦 Convenios bancarios disponibles en caja principal."
    ),
    "mat_requisitos": (
        "📋 *Requisitos de Matrícula*\n\n"
        "Para completar tu matrícula necesitas:\n\n"
        "✅ Paz y salvo financiero vigente\n"
        "✅ Carné estudiantil al día\n"
        "✅ Sin materias pendientes de cancelar\n"
        "✅ Foto actualizada en el sistema\n"
        "✅ Sin sanciones disciplinarias activas\n\n"
        "📍 Verificación presencial:\n"
        "Oficina de Registro y Control, Bloque A"
    ),
    "mat_asesor": (
        "👤 *Asesor de Matrículas*\n\n"
        "Nuestros asesores te atienden con gusto:\n\n"
        "📞 Teléfono: (601) 123-4567 ext. 101\n"
        "✉️ Email: matriculas@universidad.edu\n"
        "💬 Chat: portal.universidad.edu/chat\n"
        "🕐 Horario: Lun-Vie 8:00am - 5:00pm\n\n"
        "📍 Atención presencial:\n"
        "Bloque A, Oficina 105"
    ),

    # ── CERTIFICADOS ──────────────────────────────────────────────────────────
    "cert_academico": (
        "🎓 *Certificado Académico*\n\n"
        "⏱️ Tiempo de entrega: 3-5 días hábiles\n"
        "💵 Costo: $15,000\n\n"
        "📝 *Cómo solicitarlo:*\n"
        "1️⃣ Portal estudiantil > Servicios > Certificados\n"
        "2️⃣ Selecciona *Certificado Académico*\n"
        "3️⃣ Realiza el pago en línea\n"
        "4️⃣ Recíbelo en tu correo institucional\n\n"
        "📄 También disponible en Registro y Control."
    ),
    "cert_notas": (
        "📊 *Certificado de Notas*\n\n"
        "⏱️ Disponible de inmediato (descarga digital)\n"
        "💵 Costo: $10,000 (versión sellada)\n\n"
        "🌐 *Descarga gratuita en:*\n"
        "portal.universidad.edu > Mis documentos\n\n"
        "✅ El certificado digital tiene validez oficial.\n"
        "📄 Versión física sellada en Registro y Control."
    ),
    "cert_matricula": (
        "📋 *Certificado de Matrícula*\n\n"
        "⏱️ Disponible inmediatamente tras el pago\n"
        "💵 Costo: $8,000\n\n"
        "🌐 *Descárgalo en:*\n"
        "portal.universidad.edu > Mis documentos\n\n"
        "✅ Válido para:\n"
        "• EPS y sistemas de salud\n"
        "• Entidades bancarias\n"
        "• Trámites oficiales"
    ),

    # ── SOPORTE ───────────────────────────────────────────────────────────────
    "sop_contrasena": (
        "🔑 *Recuperar Contraseña del Portal*\n\n"
        "Sigue estos pasos:\n\n"
        "1️⃣ Ve a *portal.universidad.edu*\n"
        "2️⃣ Clic en *¿Olvidaste tu contraseña?*\n"
        "3️⃣ Ingresa tu correo institucional\n"
        "4️⃣ Revisa tu bandeja (incluye carpeta spam)\n"
        "5️⃣ Sigue el enlace y crea tu nueva clave\n\n"
        "⏱️ El correo llega en máximo 5 minutos.\n"
        "📞 ¿No funciona? Llama al ext. 200"
    ),
    "sop_acceso": (
        "🚫 *Problemas de Acceso al Sistema*\n\n"
        "Posibles causas y soluciones:\n\n"
        "❗ *Contraseña incorrecta*\n"
        "→ Usa la opción de recuperación\n\n"
        "❗ *Usuario bloqueado* (3+ intentos fallidos)\n"
        "→ Contacta soporte para desbloqueo\n\n"
        "❗ *Cuenta suspendida*\n"
        "→ Verifica tu estado financiero\n\n"
        "📞 Soporte: (601) 123-4567 ext. 200\n"
        "✉️ soporte@universidad.edu\n"
        "🕐 Lun-Vie 8:00am - 6:00pm"
    ),
    "sop_ticket": (
        "🎫 *Abrir Ticket de Soporte Técnico*\n\n"
        "Para un seguimiento eficiente de tu caso:\n\n"
        "🌐 *soporte.universidad.edu*\n"
        "1️⃣ Clic en *Nuevo ticket*\n"
        "2️⃣ Selecciona la categoría del problema\n"
        "3️⃣ Describe el problema con detalle\n"
        "4️⃣ Adjunta capturas de pantalla\n"
        "5️⃣ Guarda tu número de ticket 📌\n\n"
        "⏱️ Tiempo de respuesta: 24-48 horas hábiles."
    ),

    # ── PQRS ──────────────────────────────────────────────────────────────────
    "pqrs_peticion": (
        "📌 *Petición*\n\n"
        "Una petición es una solicitud respetuosa de información, documentos o acciones específicas.\n\n"
        "📝 *Cómo radicarla:*\n"
        "• Portal: portal.universidad.edu > PQRS\n"
        "• Presencial: Bloque B, Oficina de Atención al Ciudadano\n"
        "• Email: pqrs@universidad.edu\n\n"
        "⏱️ Tiempo de respuesta: *15 días hábiles*\n"
        "📧 Confirmación enviada al correo institucional."
    ),
    "pqrs_queja": (
        "😤 *Queja*\n\n"
        "Una queja expresa inconformidad con la prestación de un servicio.\n\n"
        "📝 *Cómo radicarla:*\n"
        "• Portal: portal.universidad.edu > PQRS\n"
        "• Presencial: Bloque B, Oficina de Atención\n"
        "• Email: pqrs@universidad.edu\n\n"
        "⏱️ Tiempo de respuesta: *15 días hábiles*\n\n"
        "ℹ️ Incluye fecha, lugar y descripción detallada del hecho."
    ),
    "pqrs_reclamo": (
        "⚠️ *Reclamo*\n\n"
        "Un reclamo exige el reconocimiento o corrección de un derecho vulnerado.\n\n"
        "📝 *Para radicarlo:*\n"
        "1️⃣ Reúne evidencias y documentos de soporte\n"
        "2️⃣ Portal: portal.universidad.edu > PQRS\n"
        "3️⃣ O acude al Defensor Estudiantil\n\n"
        "📞 Defensor Estudiantil: (601) 123-4567 ext. 305\n"
        "⏱️ Respuesta: *15 días hábiles*"
    ),
    "pqrs_sugerencia": (
        "💡 *Sugerencia*\n\n"
        "¡Tus ideas nos ayudan a mejorar!\n\n"
        "📝 *Comparte tu sugerencia en:*\n"
        "• Portal: portal.universidad.edu > PQRS\n"
        "• Buzón físico: Bloques A y B\n"
        "• Email: mejoras@universidad.edu\n\n"
        "✅ Todas las sugerencias son revisadas mensualmente\n"
        "por el Comité de Calidad Institucional.\n\n"
        "¡Gracias por contribuir a nuestra mejora continua! 🙌"
    ),

    # ── HORARIOS ──────────────────────────────────────────────────────────────
    "hor_consultar": (
        "🔍 *Consultar tu Horario*\n\n"
        "Accede a tu horario personalizado:\n\n"
        "🌐 *portal.universidad.edu > Mi Horario*\n\n"
        "👤 Usuario: número de documento\n"
        "🔑 Clave: fecha de nacimiento (DDMMAAAA)\n\n"
        "📱 También disponible en la *App Universitaria*\n"
        "→ Descárgala en Play Store o App Store."
    ),
    "hor_descargar": (
        "📥 *Descargar Horario en PDF*\n\n"
        "Sigue estos pasos:\n\n"
        "1️⃣ Ingresa a *portal.universidad.edu*\n"
        "2️⃣ Ve a la sección *Mi Horario*\n"
        "3️⃣ Clic en el botón *📄 Descargar PDF*\n"
        "4️⃣ El archivo se descarga automáticamente\n\n"
        "📱 Desde la app: Horario > Exportar > PDF\n\n"
        "✅ El PDF es válido como horario oficial certificado."
    ),
    "hor_problema": (
        "⚠️ *Reportar Problema con Horario*\n\n"
        "Problemas frecuentes y cómo resolverlos:\n\n"
        "❗ *Choque de materias*\n"
        "→ Dirígete a Registro y Control\n\n"
        "❗ *Salón asignado incorrecto*\n"
        "→ Notifica a tu coordinador de carrera\n\n"
        "❗ *Docente no aparece en el sistema*\n"
        "→ Contacta directamente a tu facultad\n\n"
        "📞 Registro y Control: (601) 123-4567 ext. 150\n"
        "🕐 Lun-Vie 8:00am - 5:00pm"
    ),

    # ── ASESOR ────────────────────────────────────────────────────────────────
    "hablar_asesor": (
        "👤 *Hablar con un Asesor*\n\n"
        "Nuestros asesores están listos para atenderte:\n\n"
        "📞 Línea principal: (601) 123-4567\n"
        "✉️ Email: info@universidad.edu\n"
        "💬 Chat en vivo: portal.universidad.edu/chat\n\n"
        "🕐 *Horarios de atención:*\n"
        "Lun-Vie: 8:00am - 6:00pm\n"
        "Sábados: 9:00am - 1:00pm\n\n"
        "Un asesor se comunicará contigo en breve. 🙏"
    ),
}

# ── Sets de IDs para lookup rápido ────────────────────────────────────────────

SUBMENU_IDS:  frozenset[str] = frozenset(SUBMENUS.keys())
CONTENT_IDS:  frozenset[str] = frozenset(CONTENT.keys())
ENCUESTA_IDS: frozenset[str] = frozenset(ENCUESTA_RESPUESTAS.keys())