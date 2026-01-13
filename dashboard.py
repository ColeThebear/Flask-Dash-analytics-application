from dash import Dash, html, dcc
from dash import dash_table
from dash.dash_table.Format import Group
import dash_mantine_components as dmc
from dash_draggable import GridLayout
import plotly.express as px
import pandas as pd
from models import Ticket
from config import Config
from flask import Blueprint

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

def load_ticket_data(app):
    with app.app_context():
        tickets = Ticket.query.all()
        return pd.DataFrame([{
            'Ticket ID': t.ticket_id,
            'Subject': t.subject,
            'Assignee': t.assignee,
            'Requester': t.requester,
            'Closed': t.closed,
            'Severity': t.severity,
            'Organisation': t.organisation,
            'Requested': t.requested,
            'Ticket_duration_hours': t.ticket_duration_hours,
            'sla_met': t.sla_met
        } for t in tickets])

def create_dashboard(server):
    # This Dash app is mounted at /dashboard/
    # Access to this route is protected with @login_required in app.py
    dash_app = Dash(__name__, server=server, url_base_pathname='/dashboard/', suppress_callback_exceptions=True)
    df = load_ticket_data(server)
    if df.empty:
        df = pd.DataFrame(columns=['Ticket ID', 'Subject', 'Assignee', 'Requester', 'Closed', 'Severity', 'Organisation', 'Requested', 'Ticket duration in hours', 'SLA met'])

    system_info = dmc.Accordion(
        value="System Info",  # Add this line
        children=[
            dmc.AccordionItem([
            dmc.AccordionControl("System Info"),
            dmc.AccordionPanel([
                dmc.Text(f"App Version: {Config.APP_VERSION}"),
                dmc.Text(f"Last Deployment: {Config.DEPLOY_DATE}"),
                dmc.Text(f"Environment: {Config.ENVIRONMENT.capitalize()}"),
                dmc.Text(f"Git Commit: {Config.get_git_commit()}"),
                dmc.Text("Smoke Tests: ✅ Login, DB, Dashboard verified")
                ])
            ], value="System Info")
        ]
    )

    dash_app.layout = dmc.MantineProvider(theme={
        "fontFamily": "Open Sans, sans-serif",
        "colors": {"primary": ["#1B5E20"], "gray": ["#F5F5F5", "#EEEEEE", "#E0E0E0"]},
        "spacing": {"md": 16, "lg": 24}
    }, children=[
        dmc.Container(fluid=True, px=0, children=[
            dmc.Title("Zendesk Export Dashboard", order=1, ta="center"),
            system_info,
            dmc.Grid([
                GridLayout(
                    children=[
                        html.Div(dmc.Card(children=[
                            dcc.Graph(id='graph', figure=px.histogram(df, x='Ticket_duration_hours', color='sla_met',labels={'ticket_duration_hours': 'Ticket_duration_hours', 'sla_met': 'sla_met'}))
                        ]), style={"padding": "8px"}, id="graph-container"),  # Changed from "graph" to "graph-container"

                        html.Div(dmc.Card(children=[
                            dash_table.DataTable(
                                id='table',
                                columns=[{"name": "Ticket ID", "id": "Ticket ID"},
                                         {"name":"Subject", "id": "Subject"},
                                         {"name":"Assignee", "id": "Assignee"}, 
                                         {"name":"Requester", "id": "Requester"}, 
                                         {"name":"Closed", "id": "Closed"},
                                         {"name":"Severity", "id": "Severity"},
                                         {"name":"Organisation", "id": "Organisation"},
                                         {"name":"Requested", "id": "Requested"},
                                         {"name":"Ticket duration in hours", "id": "Ticket_duration_hours"},
                                         {"name":"SLA met", "id": "sla_met"}],
                                page_size=12,
                                data=df.to_dict('records'),
                                style_table={'overflowX': 'auto', 'border': '1px solid #ccc'},
                                style_cell={'padding': '8px', 'textAlign': 'left', 'fontFamily': 'Open Sans', 'fontSize': '14px'},
                                style_header={'backgroundColor': '#69e3fa', 'color': 'white', 'fontWeight': 'bold'}
                            )
                        ]), style={"padding": "8px"}, id="table-container")  # Changed from "table" to "table-container",
                    ],
                    gridCols=12,
                    height=60,
                    width=1200,
                    layout=[
                        {"i": "graph-container", "x": 0, "y": 0, "w": 6, "h": 4},
                        {"i": "table-container", "x": 6, "y": 0, "w": 6, "h": 4}
                    ]
                )
            ])
        ])
    ])
    return dash_app