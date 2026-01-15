from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, TargetDriftPreset

def check_monitoring(reference_data, current_data):
    """
    reference_data: Dados usados no treino
    current_data: Dados coletados na produção na última semana
    """
    drift_report = Report(metrics=[
        DataDriftPreset(),
        TargetDriftPreset(),
    ])

    drift_report.run(reference_data=reference_data, current_data=current_data)
    drift_report.save_html("monitor/report.html")
    
    result = drift_report.as_dict()
    if result["metrics"][0]["result"]["dataset_drift"]:
        print("ALERTA: Drift detectado! Iniciar processo de re-treino.")