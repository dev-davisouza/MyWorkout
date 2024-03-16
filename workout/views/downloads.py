# File designated for the functions the user can download it workout
from django.http import HttpResponse, FileResponse
import io
import xlwt
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from workout.models import Workout


def download_myworkout_as_xls(request, slug):
    object = Workout.objects.get(slug=slug, user=request.user)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{object.name}.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Exercises', 'Sets', 'Reps margin']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    relationships = object.set_exercise_relationships.all()
    rows = [[set.exercise.name, set.sets, set.get_reps_margin()] for set in relationships]
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


def download_myworkout_as_pdf(request, slug):
    # Create a Bytestream buffer
    buffer = io.BytesIO()

    # Create a canvas
    c = canvas.Canvas(buffer, pagesize=letter, bottomup=0)

    # Create a text object
    text_object = c.beginText()
    text_object.setTextOrigin(inch, inch)
    text_object.setFont("Helvetica", 14)

    # Blank lines
    lines = []

    # Designate the model
    workout = Workout.objects.get(slug=slug, user=request.user)

    # Loop
    for set in workout.set_exercise_relationships.all():
        lines.append(f"{set.exercise.name} - {set.sets} sets - {set.get_reps_margin()} reps;")

    for line in lines:
        text_object.textLine(line)

    # Finishing Up
    c.drawText(text_object)
    c.showPage()
    c.save()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename=f'{workout.name}.pdf' )
