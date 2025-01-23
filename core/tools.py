from core import utils


def get_tools(user):
    if not user:
        generales = False
    else:
        generales = utils.get_generales(user)
        
    chatbot = utils.pg_fetch(table_name="app_chatbot", filter=["activo", True], fields="*")[0]

    (id, sys_prompt, energux_prompt, myros_prompt, servidores_prompt, 
    fastos_pagus_prompt, nombre, activo, X, facebook, instagram, 
    telegram, whatsapp, generales_prompt, cuestionarios_prompt) = chatbot

    get_datetime = {
        "type": "function",
        "function": {
            "name": "get_datetime",
            "description": "Consulta la fecha actual",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    }
    
    redes_sociales = {
        "type": "function",
        "function": {
            "name": "redes_sociales",
            "description": "Consulta las redes sociales de la empresa",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    }

    get_generales_tool = {
        "type": "function",
        "function": {
            "name": "get_generales_tool",
            "description": "Consulta las generales asociadas a un usuario",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    }

    crear_generales = {
        "type": "function",
        "function": {
            "name": "crear_generales",
            "description": generales_prompt,
            "parameters": {
                "type": "object",
                "properties": {
                    "nombre_empresa": {
                        "type": "string",
                        "description": "Nombre de la empresa a la que pertenece el usuario."
                    },
                    "dir": {
                        "type": "string",
                        "description": "Dirección de la empresa a la que pertenece el usuario."
                    },
                    "mun": {
                        "type": "string",
                        "description": "Municipio al que pertenece la empresa del usuario."
                    },
                    "prov": {
                        "type": "string",
                        "description": "Provincia a la que pertenece la empresa del usuario."
                    },
                    "email": {
                        "type": "string",
                        "description": "Correo electrónico de la empresa del usuario."
                    },
                    "tel": {
                        "type": "string",
                        "description": "Teléfono de la empresa del usuario."
                    },
                    "nombre": {
                        "type": "string",
                        "description": "Nombre del usuario."
                    },
                    "apellidos": {
                        "type": "string",
                        "description": "Apellidos del usuario."
                    },
                    "cargo": {
                        "type": "string",
                        "description": "Cargo del usuario en su empresa."
                    }
                },
                "required": ["nombre_empresa", "dir", "mun", "prov", "email", "tel", "nombre", "apellidos", "cargo"]
            }
        }
    }
    
    info_contacto = {
        "type": "function",
        "function": {
            "name": "info_contacto",
            "description": "Consulta la información de contacto de Soluciones DTeam",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    }
    
    cuestionario = {
        "type": "function",
        "function": {
            "name": "cuestionario",
            "description": cuestionarios_prompt,
            "parameters": {
                "type": "object",
                "properties": {
                    "service_name": {
                        "type": "string",
                        "description": "Nombre del servicio solicitado por el usuario",
                    },
                },
                "required": ["service_name"],
            },
        },
    }
    
    clean_chat = {
        "type": "function",
        "function": {
            "name": "clean_chat",
            "description": "Borra la conversación actual. Se limpia el chat",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    }
    
    Energux = {
        "type": "function",
        "function": {
            "name": "Energux",
            "description": energux_prompt,
            "parameters": {
                "type": "object",
                "properties": {
                    "cantidad_usuarios": {"type": "integer", "description": "Cantidad de usuarios que trabajarán con el sistema."},
                    "entidad_consolidadora": {"type": "boolean", "description": "¿Su empresa funciona como una entidad que consolida los datos de otras entidades?"},
                    "entidad_subordinada": {"type": "boolean", "description": "¿Su empresa está subordinada a una entidad que consolida los datos de otras entidades?"},
                    "monedas_trabajo": {"type": "array", "items": {"type": "string"}, "description": "Tipos de moneda con que trabaja la Empresa"},
                    "centros_costo": {"type": "integer", "description": "Cantidad de centros de costo"},
                    "tarjetas_combustibles": {"type": "integer", "description": "Cantidad de tarjetas de combustible"},
                    "equipos": {"type": "integer", "description": "Cantidad de equipos"},
                    "choferes": {"type": "integer", "description": "Cantidad de choferes"},
                    "control_hojas_rutas": {"type": "boolean", "description": "¿Control de hojas de ruta?"},
                    "plan_consumo_vehiculos": {"type": "boolean", "description": "¿Plan de consumo de vehículos?"},
                    "modelo_portadores": {"type": "string", "description": "¿Utilización de los modelos para los Portadores(5073-CDA002)?"},
                    "sistema_contable_automatizado": {"type": "boolean", "description": "¿Sistema contable automatizado?"},
                    "sistema_contable_utilizado": {"type": "string", "description": "Sistema contable utilizado"},
                    "portadores": {"type": "string", "description": "Portadores que utilizan. ej: Diésel, Gasolinas"},
                    "plan_mensual_portador": {"type": "boolean", "description": "¿Hay definido un plan mensual para cada portador?"},
                    "registro_contadores_electricos": {"type": "boolean", "description": "¿Tienen registro de contadores eléctricos?"},
                    "registro_transformadores_electricos": {"type": "boolean", "description": "¿Tienen registro de transformadores eléctricos?"},
                    "plan_consumo_electrico": {"type": "boolean", "description": "¿Tienen definidos planes de consumo eléctrico?"},
                    "cuentas_control_combustible": {"type": "boolean", "description": "Descripción de las cuentas relacionadas con el control de combustible en la entidad"}
                },
                "required": ["cantidad_usuarios", "entidad_consolidadora", "entidad_subordinada", "monedas_trabajo", "centros_costo", "tarjetas_combustibles", "equipos", "choferes", "control_hojas_rutas", "plan_consumo_vehiculos", "modelo_portadores", "sistema_contable_automatizado", "sistema_contable_utilizado", "portadores", "plan_mensual_portador", "registro_contadores_electricos", "registro_transformadores_electricos", "plan_consumo_electrico", "cuentas_control_combustible"]
            }
        }
    }
    
    Myros = {
        "type": "function",
        "function": {
            "name": "Myros",
            "description": myros_prompt,
            "parameters": {
                "type": "object",
                "properties": {
                    "cantidad_usuarios": {
                        "type": "integer",
                        "description": "Cantidad de usuarios que trabajarán con el sistema (Especialista de Negocios, comercial, Asesor Jurídico)."
                    },
                    "cantidad_pc": {
                        "type": "integer",
                        "description": "Cantidad de PC en uso."
                    },
                    "entidad_consolidadora": {
                        "type": "boolean",
                        "description": "¿Su empresa funciona como una entidad que consolida los datos de otras entidades?"
                    },
                    "monedas_trabajo": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "Tipos de moneda con que trabaja la Empresa (e.g., CUC, CUP)."
                    },
                    "contratos_a_personas_naturales": {
                        "type": "boolean",
                        "description": "¿Se emiten contratos a personas Naturales?"
                    },
                    "registro_contratos_actualizado": {
                        "type": "boolean",
                        "description": "¿Mantienen un registro de Contratos actualizado?"
                    },
                    "registro_clientes_proveedores_actualizado": {
                        "type": "boolean",
                        "description": "¿Mantienen un registro de clientes y proveedores actualizado?"
                    },
                    "registro_productos_servicios": {
                        "type": "boolean",
                        "description": "¿Mantienen un registro de los productos y servicios que ofertan y/o reciben?"
                    },
                    "sistema_contable_versat": {
                        "type": "boolean",
                        "description": "¿Cuentan con el Sistema Contable Versat Sarasola?"
                    },
                    "cuentas_gestion_contractual": {
                        "type": "object",
                        "properties": {
                            "cuenta_cup": {
                                "type": "string",
                                "description": "Cuenta CUP relacionada con la gestión contractual."
                            },
                            "cuenta_cuc": {
                                "type": "string",
                                "description": "Cuenta CUC relacionada con la gestión contractual."
                            }
                        },
                        "required": ["cuenta_cup", "cuenta_cuc"]
                    }
                },
                "required": [
                    "cantidad_usuarios",
                    "cantidad_pc",
                    "entidad_consolidadora",
                    "monedas_trabajo",
                    "contratos_a_personas_naturales",
                    "registro_contratos_actualizado",
                    "registro_clientes_proveedores_actualizado",
                    "registro_productos_servicios",
                    "sistema_contable_versat",
                    "cuentas_gestion_contractual"
                ]
            }
        }
    }
    
    Servidores = {
        "type": "function",
        "function": {
            "name": "Servidores",
            "description": servidores_prompt,
            "parameters": {
                "type": "object",
                "properties": {
                    "modo_conexion_red": {
                        "type": "string",
                        "enum": ["ADSL", "Modem", "Fibra óptica", "Otro"],
                        "description": "Modo de conexión a la red"
                    },
                    "nivel_conexion": {
                        "type": "object",
                        "properties": {
                            "intranet": {"type": "boolean", "description": "¿Conexión a Intranet?"},
                            "internet": {"type": "boolean", "description": "¿Conexión a Internet?"}
                        },
                        "description": "Nivel de conexión"
                    },
                    "cantidad_host_fisico": {
                        "type": "integer",
                        "description": "Cantidad de host físicos"
                    },
                    "cantidad_host_virtuales": {
                        "type": "integer",
                        "description": "Cantidad de host virtuales"
                    },
                    "servicios_a_instalar": {
                        "type": "object",
                        "properties": {
                            "controlador_dominio": {"type": "boolean", "description": "¿Instalar Controlador de Dominio?"},
                            "servidor_salvas": {"type": "boolean", "description": "¿Instalar Servidor de Salvas?"},
                            "proxy": {"type": "boolean", "description": "¿Instalar Proxy?"},
                            "servidor_correo": {"type": "boolean", "description": "¿Instalar Servidor de Correo?"},
                            "servidores_web": {"type": "boolean", "description": "¿Instalar Servidores Web?"},
                            "ftp": {"type": "boolean", "description": "¿Instalar FTP?"},
                            "jabber": {"type": "boolean", "description": "¿Instalar Jabber?"},
                            "servidor_nube": {"type": "boolean", "description": "¿Instalar Servidor Nube?"},
                            "wsus": {"type": "boolean", "description": "¿Instalar WSUS?"},
                            "cortafuego": {"type": "boolean", "description": "¿Instalar Cortafuego?"},
                            "smtp_relay": {"type": "boolean", "description": "¿Instalar SMTP Relay?"},
                            "otros": {"type": "boolean", "description": "¿Instalar otros servicios?"}
                        },
                        "description": "Servicios a instalar"
                    },
                    "ip_reservadas_dhcp": {
                        "type": "boolean",
                        "description": "¿IP reservadas en el DHCP?"
                    }
                },
                "required": [
                    "modo_conexion_red",
                    "nivel_conexion",
                    "cantidad_host_fisico",
                    "cantidad_host_virtuales",
                    "servicios_a_instalar",
                    "ip_reservadas_dhcp"
                ]
            }
        }
    }
    
    tools_con_generales = [get_datetime, redes_sociales, get_generales_tool, crear_generales, 
                           info_contacto, cuestionario, clean_chat, Energux, Myros, Servidores]

    tools_sin_generales = [get_datetime, crear_generales, get_generales_tool, cuestionario, clean_chat]
    
    return tools_con_generales if generales else tools_sin_generales
