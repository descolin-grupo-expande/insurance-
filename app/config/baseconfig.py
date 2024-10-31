# -*- coding: utf-8 -*-
"""
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

from datetime import timedelta
from .localconfig import LocalConfig

class BaseConfig(LocalConfig):
    
    ###########################################################################
    # API
    ###########################################################################
    API_PER_PAGE = 50
    ALL_LIMIT = 1000

    ############################
    # Assistance Process Messages
    ############################
    IN_APP_TICKET_TYPE_1_COMMENT = "Caso y ticket generado desde la app de asistencia por cliente"
    IN_APP_TICKET_TYPE_2_COMMENT = "Asignacion del proveedor generado desde la app de asistencia por proveedor"
    IN_APP_TICKET_TYPE_3_COMMENT = "Notificacion automatica por utilizar la app de asistencia"
    IN_APP_TICKET_TYPE_4_COMMENT = "Proveedor ha marcado su llegada desde la app de asistencia"
    IN_APP_TICKET_TYPE_5_COMMENT = "Proveedor indica que el caso ha sido terminado con exito"
    IN_APP_CLIENT_REVIEW_ES = "Gracias por la respuesta"
    IN_APP_CLIENT_REVIEW_EN = "Thanks for the feedback"
    IN_APP_PROVIDER_CASE_ASSIGN = "case assign successfull"

    IN_APP_TD_TICKET_TYPE_1_COMMENT = "Caso y ticket generado desde la app de Teledoctor por cliente"
    IN_APP_TD_TICKET_TYPE_2_COMMENT = "Asignacion del proveedor generado desde Apolo11 por Medico"
    IN_APP_TD_TICKET_TYPE_3_COMMENT = "Notificacion automatica por utilizar la app de Teledoctor"
    IN_APP_TD_TICKET_TYPE_4_COMMENT_CALL = "Medico contesto la llamada"
    IN_APP_TD_TICKET_TYPE_4_COMMENT_CHAT = "Medico atendio el chat"


    # OPERATOR
    OPERATOR = 'operator'
    ASSISTANCE_OPERATOR_VIP = 'assistance_operator_vip'
    
    # DISPACHER
    ASSISTANCE_DISPATCHER = 'assistance_dispatcher'
    ASSISTANCE_DISPATCHER_VIP = 'assistance_dispatcher_vip'
    ASSISTANCE_DISPATCHER_MEDICAL = 'assistance_dispatcher_medical'
    ASSISTANCE_DISPATCHER_VIAL = 'assistance_dispatcher_vial'
    
    # SERVICES ATTENDED
    SERVICES_ATTENDED_BY_CURRENT_USER = ["Legal"]
    SERVICES_ATTENDED_TO_VIAL = ["Vial", "Autos Vial", "Especiales Vial", "Funeraria", "Hogar", "Veterinaria"]
    SERVICES_ATTENDED_TO_MEDICAL = [
        "Médica",
        "Examen",
        "Dental",
        "Especiales Medicas",
        "Dental-Diagnostico",
        "Dental-Operatoria",
        "Dental-Odontopediatria",
        "Dental-Radiologia",
        "Dental-Prevencion",
        "Dental-Cirugia",
        "Dental-Endodoncia",
        "Dental-Periodoncia",
        "Dental-Protesis",
        "Dental-Urgencia Bucodental",
        "Dental telefónico -AS",
        "Dental Presencial-AS",
        "Diagnóstico - SEG",
        "Operatoria - SEG",
        "Odontopediatría - SEG",
        "Radiología - SEG",
        "Prevención - SEG",
        "Endodoncia - SEG",
        "Periodoncia - SEG",
        "Prótesis - SEG",
        "Urgencia inespecífica - SEG",
        "Dental telefónico -SEG",
        "Dental Presencial-SEG"
    ]

    """Docstring for BaseConfig. """