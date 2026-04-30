from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.http import HttpResponse

def generate_route_pdf(route):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="route_{route.id}.pdf"'
    
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    
    p.setFont("Helvetica-Bold", 18)
    p.drawString(50, height - 50, f"Маршрут: {route.title}")
    
    p.setFont("Helvetica", 12)
    p.drawString(50, height - 80, f"Автор: {route.author.username}")
    p.drawString(50, height - 100, f"Страны: {route.countries}")
    p.drawString(50, height - 120, f"Города: {route.cities or 'Не указаны'}")
    p.drawString(50, height - 140, f"Даты: {route.start_date} - {route.end_date}")
    p.drawString(50, height - 160, f"Бюджет: {route.budget or 'Не указан'} ₽")
    
    # Описание
    p.drawString(50, height - 190, "Описание:")
    text = route.description[:500] if route.description else "Нет описания"
    p.drawString(50, height - 210, text)
    
    p.showPage()
    p.save()
    return response