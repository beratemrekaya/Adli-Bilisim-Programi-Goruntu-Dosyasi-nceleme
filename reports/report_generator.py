# reports/report_generator.py

import os
from datetime import datetime

class ReportGenerator:
    def __init__(self):
        # Rapor şablonlarını veya çıktı dizinlerini burada tanımlayabilirsiniz.
        self.report_output_dir = "reports/generated_reports"
        os.makedirs(self.report_output_dir, exist_ok=True)

    def generate_html_report(self, analysis_data, output_path):
        """
        Analiz verilerini kullanarak bir HTML raporu oluşturur.
        """
        report_title = f"Adli Analiz Raporu - {analysis_data.get('filename', 'Genel Rapor')}"
        report_date = analysis_data.get("report_date", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        # HTML yapısını oluşturmaya başla
        html_content = f"""
        <!DOCTYPE html>
        <html lang="tr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{report_title}</title>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; background-color: #f4f7f6; }}
                .container {{ width: 80%; margin: 20px auto; background: #fff; padding: 30px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }}
                h1, h2, h3 {{ color: #0056b3; border-bottom: 2px solid #e0e0e0; padding-bottom: 10px; margin-top: 30px; }}
                h1 {{ text-align: center; color: #004085; font-size: 2.2em; }}
                h2 {{ font-size: 1.8em; }}
                h3 {{ font-size: 1.4em; color: #007bff; }}
                p {{ margin-bottom: 10px; }}
                .section {{ background-color: #f9f9f9; border: 1px solid #eee; border-radius: 5px; padding: 15px; margin-bottom: 20px; }}
                .warning {{ color: #d9534f; font-weight: bold; }}
                .info {{ color: #337ab7; }}
                .success {{ color: #5cb85c; }}
                pre {{ background-color: #eef; padding: 10px; border-radius: 5px; overflow-x: auto; white-space: pre-wrap; word-wrap: break-word; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #007bff; color: white; }}
                .footer {{ text-align: center; margin-top: 40px; font-size: 0.9em; color: #777; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>{report_title}</h1>
                <p><strong>Rapor Tarihi:</strong> {report_date}</p>
                <p><strong>Analiz Edilen Dosya:</strong> {analysis_data.get('file_path', 'N/A')}</p>
        """

        # Meta Veri Analizi Sonuçları
        html_content += "<h2>Meta Veri Analizi</h2>"
        metadata_results = analysis_data.get("metadata_results", {})
        if metadata_results:
            html_content += "<div class='section'>"
            html_content += f"<p><strong>Oluşturma Tarihi:</strong> {metadata_results.get('creation_date', 'Yok')}</p>"
            html_content += f"<p><strong>Değiştirme Tarihi:</strong> {metadata_results.get('modification_date', 'Yok')}</p>"
            html_content += f"<p><strong>Dosya Boyutu:</strong> {metadata_results.get('file_size', 'Yok')}</p>"
            html_content += f"<p><strong>Kamera Modeli:</strong> {metadata_results.get('camera_model', 'Yok')}</p>"
            html_content += f"<p><strong>Yazılım:</strong> {metadata_results.get('software', 'Yok')}</p>"
            html_content += f"<p><strong>GPS Koordinatları:</strong> {metadata_results.get('gps_coordinates', 'Yok')}</p>"
            html_content += f"<p><strong>Tahmini Adres:</strong> {metadata_results.get('estimated_address', 'Yok')}</p>"
            
            if metadata_results.get('manipulation_warnings'):
                html_content += "<p class='warning'><strong>Manipülasyon Uyarıları:</strong></p><ul>"
                for warning in metadata_results['manipulation_warnings']:
                    html_content += f"<li>{warning}</li>"
                html_content += "</ul>"
            else:
                html_content += "<p class='success'><strong>Manipülasyon Tespiti:</strong> Herhangi bir manipülasyon izi bulunamadı.</p>"
            
            html_content += "<h3>Tüm Ham Meta Veriler</h3>"
            html_content += f"<pre>{metadata_results.get('raw_metadata', 'Yok')}</pre>"
            html_content += "</div>"
        else:
            html_content += "<p class='info'>Meta Veri Analizi sonuçları mevcut değil.</p>"

        # Görüntü Bütünlüğü Sonuçları
        html_content += "<h2>Görüntü Bütünlüğü</h2>"
        integrity_results = analysis_data.get("integrity_results", {})
        if integrity_results:
            html_content += "<div class='section'>"
            ela_result = integrity_results.get("ela_result", "Analiz Edilemedi")
            if "olası manipülasyon" in ela_result.lower() or "hata" in ela_result.lower():
                 html_content += f"<p class='warning'><strong>ELA Sonucu:</strong> {ela_result}</p>"
            else:
                 html_content += f"<p class='success'><strong>ELA Sonucu:</strong> {ela_result}</p>"
            
            html_content += f"<p><strong>Su İzleme / Gizli Veri Tespiti:</strong> {integrity_results.get('watermarking_status', 'Geliştirme aşamasında')}</p>"
            html_content += "</div>"
        else:
            html_content += "<p class='info'>Görüntü Bütünlüğü sonuçları mevcut değil.</p>"
        
        # Kamera Adliyesi Sonuçları
        html_content += "<h2>Kamera Adliyesi</h2>"
        camera_results = analysis_data.get("camera_forensics_results", {})
        if camera_results:
            html_content += "<div class='section'>"
            html_content += f"<p><strong>Üretici:</strong> {camera_results.get('manufacturer', 'Yok')}</p>"
            html_content += f"<p><strong>Model:</strong> {camera_results.get('model', 'Yok')}</p>"
            html_content += f"<p><strong>Yazılım:</strong> {camera_results.get('software', 'Yok')}</p>"
            html_content += f"<p><strong>Lens Modeli:</strong> {camera_results.get('lens_model', 'Yok')}</p>"
            html_content += f"<p><strong>Odak Uzaklığı:</strong> {camera_results.get('focal_length', 'Yok')}</p>"
            html_content += f"<p><strong>Pozlama Süresi:</strong> {camera_results.get('exposure_time', 'Yok')}</p>"
            html_content += f"<p><strong>ISO Hızı:</strong> {camera_results.get('iso_speed', 'Yok')}</p>"
            html_content += f"<p><strong>PRNU Statüsü:</strong> {camera_results.get('prnu_status', 'Geliştirme aşamasında')}</p>"
            html_content += f"<p><strong>Eşleşen Cihaz ID (PRNU Kimliği):</strong> {camera_results.get('prnu_match_id', 'Yok')}</p>"
            html_content += f"<p><strong>Optik Bozulma Analizi:</strong> {camera_results.get('optical_distortion_status', 'Geliştirme aşamasında')}</p>"
            html_content += "</div>"
        else:
            html_content += "<p class='info'>Kamera Adliyesi sonuçları mevcut değil.</p>"

        # Olay Zinciri Sonuçları
        html_content += "<h2>Olay Zinciri</h2>"
        event_chain_results = analysis_data.get("event_chain_results", {})
        if event_chain_results:
            html_content += "<div class='section'>"
            html_content += "<h3>Kronolojik Olay Akışı</h3>"
            html_content += f"<pre>{event_chain_results.get('event_chain_text', 'Olay zinciri mevcut değil.')}</pre>"
            if event_chain_results.get('map_created'):
                html_content += f"<p class='success'>Olay Konum Haritası başarıyla oluşturuldu: <a href='file:///{os.path.abspath(event_chain_results['map_file_path'])}' target='_blank'>{os.path.basename(event_chain_results['map_file_path'])}</a></p>"
            else:
                html_content += "<p class='warning'>Olay Konum Haritası oluşturulamadı veya mevcut değil.</p>"
            html_content += "</div>"
        else:
            html_content += "<p class='info'>Olay Zinciri sonuçları mevcut değil. Lütfen 'Tüm Deliller Üzerinde Olay Zinciri Analizi Yap' butonuna tıklayınız.</p>"


        html_content += f"""
                <div class="footer">
                    <p>&copy; {datetime.now().year} Adli Bilişim Platformu. Tüm hakları saklıdır.</p>
                </div>
            </div>
        </body>
        </html>
        """

        # Raporu dosyaya yaz
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            return True
        except Exception as e:
            print(f"Rapor oluşturulurken hata: {e}")
            return False