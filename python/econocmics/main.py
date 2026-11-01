import math
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                PageBreak, KeepInFrame)
from reportlab.lib import colors
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_RIGHT, TA_CENTER
from reportlab.graphics.shapes import (Drawing, Line, Rect, String, Polygon, PolyLine,
                                       Circle, Ellipse)

W = 500
IND = HexColor('#3F51B5'); TEAL = HexColor('#00897B'); ORG = HexColor('#EF6C00')
RED = HexColor('#D32F2F'); GRN = HexColor('#2E7D32'); PUR = HexColor('#7B1FA2')
BLU = HexColor('#1976D2'); PINK = HexColor('#C2185B'); YEL = HexColor('#F9A825')

def light(c, f=0.88):
    return colors.Color(c.red + (1 - c.red) * f, c.green + (1 - c.green) * f, c.blue + (1 - c.blue) * f)

body = ParagraphStyle('body', fontName='Helvetica', fontSize=9, leading=12)
small = ParagraphStyle('small', parent=body, fontSize=8, leading=10)
smallw = ParagraphStyle('smallw', parent=small, textColor=white, fontName='Helvetica-Bold')
smallc = ParagraphStyle('smallc', parent=small, alignment=TA_CENTER)

PAGE_COLORS = [IND, IND, TEAL, ORG, RED, GRN, PUR, BLU, PINK, TEAL, ORG, RED, GRN, PUR, IND]

def P(t, st=body):
    return Paragraph(t, st)

def hexs(c):
    return '#%02X%02X%02X' % (int(c.red * 255), int(c.green * 255), int(c.blue * 255))

def hdr(title, subtitle, color, num):
    left = Paragraph('<font color="white" size="19"><b>%s</b></font>' % title, body)
    right = Paragraph('<font color="white" size="8">%s</font><br/><font color="white" size="14"><b>%d / 15</b></font>' % (subtitle, num),
                      ParagraphStyle('r', parent=body, alignment=TA_RIGHT, leading=15))
    t = Table([[left, right]], colWidths=[W - 130, 130])
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), color), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                           ('TOPPADDING', (0, 0), (-1, -1), 7), ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
                           ('LEFTPADDING', (0, 0), (-1, -1), 10), ('RIGHTPADDING', (0, 0), (-1, -1), 10)]))
    return t

def sub(text, color, width=W):
    t = Table([[Paragraph('<font color="%s" size="10.5"><b>%s</b></font>' % (hexs(color), text), body)]], colWidths=[width])
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), light(color, 0.86)),
                           ('LINEBEFORE', (0, 0), (0, 0), 4, color),
                           ('TOPPADDING', (0, 0), (-1, -1), 3), ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
                           ('LEFTPADDING', (0, 0), (-1, -1), 7)]))
    return t

def bl(items, color, st=body):
    bs = ParagraphStyle('bs', parent=st, leftIndent=11, firstLineIndent=-11, spaceAfter=1.5)
    return [Paragraph('<font color="%s"><b>&bull;</b></font>&nbsp;&nbsp;%s' % (hexs(color), i), bs) for i in items]

def box(text, color, width=W, label=None):
    txt = text if not label else '<font color="%s"><b>%s</b></font> %s' % (hexs(color), label, text)
    t = Table([[Paragraph(txt, small)]], colWidths=[width])
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), light(color, 0.9)),
                           ('BOX', (0, 0), (-1, -1), 0.8, color),
                           ('TOPPADDING', (0, 0), (-1, -1), 4), ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                           ('LEFTPADDING', (0, 0), (-1, -1), 6), ('RIGHTPADDING', (0, 0), (-1, -1), 6)]))
    return t

def T(data, color, colw=None, st=small, bold_first_col=False):
    rows = []
    for ri, r in enumerate(data):
        row = []
        for ci, c in enumerate(r):
            if ri == 0:
                row.append(Paragraph(str(c), smallw))
            else:
                s = str(c)
                if bold_first_col and ci == 0:
                    s = '<b>%s</b>' % s
                row.append(Paragraph(s, st))
        rows.append(row)
    t = Table(rows, colWidths=colw, repeatRows=1)
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), color),
                           ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, light(color, 0.9)]),
                           ('GRID', (0, 0), (-1, -1), 0.4, HexColor('#B0B0B0')),
                           ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                           ('TOPPADDING', (0, 0), (-1, -1), 2.5), ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
                           ('LEFTPADDING', (0, 0), (-1, -1), 4), ('RIGHTPADDING', (0, 0), (-1, -1), 4)]))
    return t

def two(left, right, wl=W / 2 - 4, wr=W / 2 - 4, gap=8):
    t = Table([[left, right]], colWidths=[wl, wr + gap])
    t.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LEFTPADDING', (0, 0), (-1, -1), 0),
                           ('RIGHTPADDING', (0, 0), (0, 0), gap), ('RIGHTPADDING', (1, 0), (1, 0), 0),
                           ('TOPPADDING', (0, 0), (-1, -1), 0), ('BOTTOMPADDING', (0, 0), (-1, -1), 0)]))
    return t

def sp(h=5):
    return Spacer(1, h)

# ---------------------------------------------------------------- drawings
def arrow(d, pts, color, width=1.8):
    for a, b in zip(pts[:-1], pts[1:]):
        d.add(Line(a[0], a[1], b[0], b[1], strokeColor=color, strokeWidth=width))
    (x1, y1), (x2, y2) = pts[-2], pts[-1]
    ang = math.atan2(y2 - y1, x2 - x1)
    L, Wd = 8, 3.5
    p1 = (x2 - L * math.cos(ang) + Wd * math.sin(ang), y2 - L * math.sin(ang) - Wd * math.cos(ang))
    p2 = (x2 - L * math.cos(ang) - Wd * math.sin(ang), y2 - L * math.sin(ang) + Wd * math.cos(ang))
    d.add(Polygon([x2, y2, p1[0], p1[1], p2[0], p2[1]], fillColor=color, strokeColor=color))

def circular_fig():
    w, h = 500, 235
    d = Drawing(w, h)
    d.add(Rect(0, 0, w, h, fillColor=HexColor('#FFF8E1'), strokeColor=HexColor('#FFE082'), rx=8, ry=8))
    mon = HexColor('#2E7D32'); real = HexColor('#EF6C00')
    d.add(Rect(12, 92, 118, 62, fillColor=HexColor('#BBDEFB'), strokeColor=BLU, strokeWidth=1.2))
    d.add(String(71, 138, 'FIRMS', textAnchor='middle', fontName='Helvetica-Bold', fontSize=10, fillColor=BLU))
    d.add(String(71, 124, 'Produce and sell goods', textAnchor='middle', fontSize=6.8))
    d.add(String(71, 114, 'and services', textAnchor='middle', fontSize=6.8))
    d.add(String(71, 102, 'Hire factors of production', textAnchor='middle', fontSize=6.8))
    d.add(Rect(370, 92, 118, 62, fillColor=HexColor('#BBDEFB'), strokeColor=BLU, strokeWidth=1.2))
    d.add(String(429, 138, 'HOUSEHOLDS', textAnchor='middle', fontName='Helvetica-Bold', fontSize=10, fillColor=BLU))
    d.add(String(429, 124, 'Buy and consume goods', textAnchor='middle', fontSize=6.8))
    d.add(String(429, 114, 'and services', textAnchor='middle', fontSize=6.8))
    d.add(String(429, 102, 'Own and sell factors', textAnchor='middle', fontSize=6.8))
    d.add(Ellipse(250, 205, 85, 24, fillColor=HexColor('#FFE0B2'), strokeColor=ORG))
    d.add(String(250, 208, 'MARKETS FOR GOODS', textAnchor='middle', fontName='Helvetica-Bold', fontSize=8))
    d.add(String(250, 198, 'AND SERVICES', textAnchor='middle', fontName='Helvetica-Bold', fontSize=8))
    d.add(Ellipse(250, 30, 85, 24, fillColor=HexColor('#FFE0B2'), strokeColor=ORG))
    d.add(String(250, 33, 'MARKETS FOR FACTORS', textAnchor='middle', fontName='Helvetica-Bold', fontSize=8))
    d.add(String(250, 23, 'OF PRODUCTION', textAnchor='middle', fontName='Helvetica-Bold', fontSize=8))
    # money (green)
    arrow(d, [(440, 154), (440, 205), (335, 205)], mon)
    d.add(String(446, 175, 'Spending', fontSize=7.5, fillColor=mon, fontName='Helvetica-Bold'))
    arrow(d, [(165, 205), (50, 205), (50, 154)], mon)
    d.add(String(14, 175, 'Revenue', fontSize=7.5, fillColor=mon, fontName='Helvetica-Bold'))
    arrow(d, [(50, 92), (50, 30), (165, 30)], mon)
    d.add(String(6, 60, 'Wages, rent,', fontSize=7.5, fillColor=mon, fontName='Helvetica-Bold'))
    d.add(String(6, 51, 'and profit', fontSize=7.5, fillColor=mon, fontName='Helvetica-Bold'))
    arrow(d, [(335, 30), (440, 30), (440, 92)], mon)
    d.add(String(446, 60, 'Income', fontSize=7.5, fillColor=mon, fontName='Helvetica-Bold'))
    # real (orange)
    arrow(d, [(90, 154), (90, 188), (170, 188)], real)
    d.add(String(95, 172, 'Goods and services sold', fontSize=6.5, fillColor=real))
    arrow(d, [(330, 188), (400, 188), (400, 154)], real)
    d.add(String(352, 172, 'Goods and services', fontSize=6.5, fillColor=real))
    d.add(String(352, 164, 'bought', fontSize=6.5, fillColor=real))
    arrow(d, [(400, 92), (400, 48), (335, 48)], real)
    d.add(String(345, 70, 'Labor, land,', fontSize=6.5, fillColor=real))
    d.add(String(345, 62, 'and capital', fontSize=6.5, fillColor=real))
    arrow(d, [(165, 48), (90, 48), (90, 92)], real)
    d.add(String(92, 70, 'Inputs for', fontSize=6.5, fillColor=real))
    d.add(String(92, 62, 'production', fontSize=6.5, fillColor=real))
    d.add(Line(190, 120, 220, 120, strokeColor=real, strokeWidth=2))
    d.add(String(224, 118, '= Flow of goods/services', fontSize=7))
    d.add(Line(190, 106, 220, 106, strokeColor=mon, strokeWidth=2))
    d.add(String(224, 104, '= Flow of dollars', fontSize=7))
    return d

def f1(x):
    return 3000 - 0.76 * x - 0.00095 * x * x

def f2(x):
    return 2000 - 2 * (x - 700) - 0.01556 * (x - 700) ** 2

def ppf_pts():
    pts = [(x, f1(x)) for x in range(0, 701, 20)]
    pts += [(x, max(f2(x), 0)) for x in range(720, 1001, 20)]
    return pts

def ppf_fig():
    w, h = 300, 215
    d = Drawing(w, h)
    ox, oy, pw, ph = 40, 28, 245, 170
    mx = lambda x: ox + x / 1100.0 * pw
    my = lambda y: oy + y / 3400.0 * ph
    poly = [mx(0), my(0)]
    for x, y in ppf_pts():
        poly += [mx(x), my(y)]
    poly += [mx(1000), my(0)]
    d.add(Polygon(poly, fillColor=HexColor('#C8E6C9'), strokeColor=None))
    d.add(Line(ox, oy, ox, oy + ph + 6, strokeColor=colors.black))
    d.add(Line(ox, oy, ox + pw + 6, oy, strokeColor=colors.black))
    pl = []
    for x, y in ppf_pts():
        pl += [mx(x), my(y)]
    d.add(PolyLine(pl, strokeColor=GRN, strokeWidth=2.4))
    for xv in (300, 600, 700, 1000):
        d.add(String(mx(xv), oy - 10, str(xv), fontSize=7, textAnchor='middle'))
    for yv in (1000, 2000, 2200, 3000):
        d.add(String(ox - 4, my(yv) - 2, str(yv), fontSize=7, textAnchor='end'))
    d.add(String(ox + pw / 2, 3, 'Quantity of Cars', fontSize=8, textAnchor='middle', fontName='Helvetica-Bold'))
    d.add(String(4, oy + ph + 4, 'Computers', fontSize=8, fontName='Helvetica-Bold'))
    for (x, y, lab, col, dx, dy) in [(700, 2000, 'A', GRN, 6, -2), (600, 2200, 'C', GRN, -9, 4),
                                     (300, 1000, 'B', RED, 6, -2), (760, 3000, 'D', PINK, 6, -2)]:
        d.add(Circle(mx(x), my(y), 3.6, fillColor=col, strokeColor=col))
        d.add(String(mx(x) + dx, my(y) + dy, lab, fontSize=9, fontName='Helvetica-Bold', fillColor=col))
    d.add(String(mx(790), my(3000) - 2, 'Unattainable', fontSize=7, fillColor=PINK))
    d.add(String(mx(335), my(1000) - 2, 'Inefficient (inside)', fontSize=7, fillColor=RED))
    d.add(String(mx(60), my(1500), 'Attainable region', fontSize=7.5, fillColor=GRN))
    d.add(String(mx(430), my(2700), 'PPF (frontier)', fontSize=7.5, fillColor=GRN, fontName='Helvetica-Bold'))
    return d

def ppf_shift_fig():
    w, h = 300, 215
    d = Drawing(w, h)
    ox, oy, pw, ph = 40, 28, 245, 170
    mx = lambda x: ox + x / 1100.0 * pw
    my = lambda y: oy + y / 4400.0 * ph
    d.add(Line(ox, oy, ox, oy + ph + 6, strokeColor=colors.black))
    d.add(Line(ox, oy, ox + pw + 6, oy, strokeColor=colors.black))
    old = ppf_pts()
    new = [(x, y * (1 + 0.333 * (1 - (x / 1000.0) ** 2))) for x, y in old]
    pl = []
    for x, y in new:
        pl += [mx(x), my(y)]
    d.add(PolyLine(pl, strokeColor=PUR, strokeWidth=2.4))
    pl = []
    for x, y in old:
        pl += [mx(x), my(y)]
    d.add(PolyLine(pl, strokeColor=BLU, strokeWidth=2.4))
    for xv in (700, 750, 1000):
        d.add(String(mx(xv), oy - 10, str(xv), fontSize=7, textAnchor='middle'))
    for yv in (2000, 2100, 3000, 4000):
        d.add(String(ox - 4, my(yv) - 2, str(yv), fontSize=7, textAnchor='end'))
    d.add(String(ox + pw / 2, 3, 'Quantity of Cars', fontSize=8, textAnchor='middle', fontName='Helvetica-Bold'))
    d.add(String(4, oy + ph + 4, 'Computers', fontSize=8, fontName='Helvetica-Bold'))
    d.add(Circle(mx(700), my(2000), 3.6, fillColor=BLU, strokeColor=BLU))
    d.add(String(mx(700) - 10, my(2000) - 10, 'A', fontSize=9, fontName='Helvetica-Bold', fillColor=BLU))
    ey = 2132
    d.add(Circle(mx(750), my(ey), 3.6, fillColor=PUR, strokeColor=PUR))
    d.add(String(mx(750) + 6, my(ey) + 2, 'E', fontSize=9, fontName='Helvetica-Bold', fillColor=PUR))
    d.add(String(mx(90), my(3300), 'Old PPF', fontSize=8, fillColor=BLU, fontName='Helvetica-Bold'))
    d.add(String(mx(90), my(4050), 'New PPF (growth)', fontSize=8, fillColor=PUR, fontName='Helvetica-Bold'))
    arrow(d, [(mx(330), my(2800)), (mx(330), my(3250))], ORG, 1.6)
    return d

def sd_fig():
    w, h = 300, 215
    d = Drawing(w, h)
    ox, oy, pw, ph = 36, 26, 245, 168
    mx = lambda q: ox + q / 32.0 * pw
    my = lambda p: oy + p / 8.2 * ph
    d.add(Line(ox, oy, ox, oy + ph + 6, strokeColor=colors.black))
    d.add(Line(ox, oy, ox + pw + 6, oy, strokeColor=colors.black))
    d.add(Line(mx(0), my(8), mx(24), my(0), strokeColor=BLU, strokeWidth=2.4))
    d.add(Line(mx(0), my(0), mx(31), my(6.2), strokeColor=RED, strokeWidth=2.4))
    d.add(String(mx(1.2), my(8) - 8, 'D', fontSize=10, fontName='Helvetica-Bold', fillColor=BLU))
    d.add(String(mx(30), my(6.2) + 2, 'S', fontSize=10, fontName='Helvetica-Bold', fillColor=RED))
    dash = [3, 2]
    d.add(Line(ox, my(3), mx(15), my(3), strokeColor=GRN, strokeDashArray=dash))
    d.add(Line(mx(15), oy, mx(15), my(3), strokeColor=GRN, strokeDashArray=dash))
    d.add(Circle(mx(15), my(3), 4, fillColor=GRN, strokeColor=GRN))
    d.add(String(mx(15) + 6, my(3) + 3, 'E (Q=15, P=$3)', fontSize=7.5, fontName='Helvetica-Bold', fillColor=GRN))
    d.add(Line(mx(9), my(5), mx(25), my(5), strokeColor=ORG, strokeWidth=1.6))
    d.add(Circle(mx(9), my(5), 3, fillColor=ORG, strokeColor=ORG))
    d.add(Circle(mx(25), my(5), 3, fillColor=ORG, strokeColor=ORG))
    d.add(String(mx(17) - 12, my(5) + 4, 'SURPLUS = 16', fontSize=7.5, fillColor=ORG, fontName='Helvetica-Bold'))
    d.add(String(mx(17) - 12, my(5) - 9, '(P = $5)', fontSize=6.5, fillColor=ORG))
    d.add(Line(mx(5), my(1), mx(21), my(1), strokeColor=PUR, strokeWidth=1.6))
    d.add(Circle(mx(5), my(1), 3, fillColor=PUR, strokeColor=PUR))
    d.add(Circle(mx(21), my(1), 3, fillColor=PUR, strokeColor=PUR))
    d.add(String(mx(9), my(1) + 4, 'SHORTAGE = 16 (P = $1)', fontSize=7.5, fillColor=PUR, fontName='Helvetica-Bold'))
    for qv in (5, 10, 15, 20, 25, 30):
        d.add(String(mx(qv), oy - 10, str(qv), fontSize=7, textAnchor='middle'))
    for pv in (1, 3, 5, 6, 8):
        d.add(String(ox - 4, my(pv) - 2, '$%d' % pv, fontSize=7, textAnchor='end'))
    d.add(String(ox + pw / 2, 3, 'Quantity (Q)', fontSize=8, textAnchor='middle', fontName='Helvetica-Bold'))
    d.add(String(4, oy + ph + 4, 'Price (P)', fontSize=8, fontName='Helvetica-Bold'))
    return d

def clipline(fn):
    pts = []
    for i in range(0, 101):
        x = i / 100.0
        y = fn(x)
        if 0.02 <= y <= 0.98 and 0.03 <= x <= 0.97:
            pts.append((x, y))
    return pts

def shift_panel(title, dshift, sshift, ptxt, qtxt, color):
    w, h = 118, 118
    d = Drawing(w, h)
    ox, oy, pw, ph = 8, 18, 100, 78
    mx = lambda x: ox + x * pw
    my = lambda y: oy + y * ph
    d.add(Rect(0, 0, w, h, fillColor=light(color, 0.93), strokeColor=color, strokeWidth=0.8, rx=5, ry=5))
    d.add(Line(ox, oy, ox, oy + ph, strokeColor=colors.black, strokeWidth=0.8))
    d.add(Line(ox, oy, ox + pw, oy, strokeColor=colors.black, strokeWidth=0.8))
    D0 = lambda x: 0.9 - 0.8 * x
    S0 = lambda x: 0.1 + 0.8 * x
    Dn = lambda x: 0.9 - 0.8 * (x - dshift)
    Sn = lambda x: 0.1 + 0.8 * (x - sshift)
    def draw(fn, col, dashed=False, wd=1.6):
        pts = clipline(fn)
        if len(pts) > 1:
            ln = Line(mx(pts[0][0]), my(pts[0][1]), mx(pts[-1][0]), my(pts[-1][1]), strokeColor=col, strokeWidth=wd)
            if dashed:
                ln.strokeDashArray = [3, 2]
            d.add(ln)
    draw(D0, BLU, dashed=bool(dshift) , wd=1.4)
    draw(S0, RED, dashed=bool(sshift), wd=1.4)
    if dshift:
        draw(Dn, BLU, wd=2)
    if sshift:
        draw(Sn, RED, wd=2)
    # equilibrium points
    # solve new equilibrium
    # 0.9-0.8(x-ds) = 0.1+0.8(x-ss)  => 1.6x = 0.8 + 0.8ds + 0.8ss
    xn = (0.8 + 0.8 * dshift + 0.8 * sshift) / 1.6
    yn = 0.1 + 0.8 * (xn - sshift)
    d.add(Circle(mx(0.5), my(0.5), 2.2, fillColor=colors.grey, strokeColor=colors.grey))
    d.add(Circle(mx(xn), my(yn), 3, fillColor=color, strokeColor=color))
    d.add(String(w / 2, h - 11, title, fontSize=7.8, fontName='Helvetica-Bold', textAnchor='middle', fillColor=color))
    d.add(String(w / 2, 6, '%s | %s' % (ptxt, qtxt), fontSize=7, textAnchor='middle', fontName='Helvetica-Bold'))
    d.add(String(ox + pw - 2, oy - 1, 'Q', fontSize=6, fillColor=colors.grey))
    d.add(String(ox + 2, oy + ph - 4, 'P', fontSize=6, fillColor=colors.grey))
    return d

# ---------------------------------------------------------------- pages
pages = []

# ---- Page 1
def page1():
    f = []
    banner = Table([[Paragraph('<font color="white" size="34"><b>PRINCIPLES OF ECONOMICS</b></font><br/>'
                               '<font color="white" size="15">15-Page Colourful Revision Note</font><br/><br/>'
                               '<font color="#FFE082" size="10">BRUR CSE | Semester Examination | Based on Mankiw Ch. 4 + Lecture Chapter 2</font>',
                               ParagraphStyle('bn', parent=body, leading=38))]], colWidths=[W])
    banner.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), IND), ('TOPPADDING', (0, 0), (-1, -1), 26),
                                ('BOTTOMPADDING', (0, 0), (-1, -1), 24), ('LEFTPADDING', (0, 0), (-1, -1), 18)]))
    f += [banner, sp(10)]
    toc = [['Page', 'Topic', 'Page', 'Topic'],
           ['2', 'Definitions of Economics (Smith to Keynes)', '9', 'Related Goods + Active Learning 1'],
           ['3', 'Scarcity, Opportunity Cost, Micro vs Macro', '10', 'Supply + Market Supply'],
           ['4', 'Circular-Flow Diagram', '11', 'Supply Shifters + Active Learning 2'],
           ['5', 'Production Possibilities Frontier', '12', 'Equilibrium, Surplus, Shortage'],
           ['6', 'PPF Shift + Positive vs Normative', '13', '3-Step Method + Shift Table'],
           ['7', 'Markets, Competition, Demand', '14', 'Maths Problems + CS and PS'],
           ['8', 'Market Demand + Demand Shifters', '15', 'Price Controls, Systems, Exceptions']]
    f.append(sub('CONTENTS', IND))
    f.append(sp(4))
    f.append(T(toc, IND, colw=[34, 216, 34, 216]))
    f.append(sp(10))
    f.append(sub('HOW TO USE THIS NOTE (3 Days Plan)', TEAL))
    f += bl(['<b>Day 1:</b> Pages 2 to 6 (definitions, PPF, circular flow). Draw the PPF and circular flow 3 times from memory.',
             '<b>Day 2:</b> Pages 7 to 13 (demand, supply, equilibrium). Practice the 3-step method on 5 events.',
             '<b>Day 3:</b> Pages 14 and 15 (maths and extras). Solve all numericals without looking.',
             '<b>Last hour:</b> Read only the coloured BOX items on every page.'], TEAL)
    f.append(sp(8))
    f.append(sub('COLOUR CODE', PUR))
    legend = Table([[P('<font color="#1976D2"><b>BLUE</b></font> = Demand side'),
                     P('<font color="#D32F2F"><b>RED</b></font> = Supply side'),
                     P('<font color="#2E7D32"><b>GREEN</b></font> = Equilibrium or efficient'),
                     P('<font color="#EF6C00"><b>ORANGE</b></font> = Surplus or warning')]],
                   colWidths=[W / 4] * 4)
    legend.setStyle(TableStyle([('BOX', (0, 0), (-1, -1), 0.6, PUR), ('INNERGRID', (0, 0), (-1, -1), 0.3, PUR),
                                ('TOPPADDING', (0, 0), (-1, -1), 5), ('BOTTOMPADDING', (0, 0), (-1, -1), 5)]))
    f += [sp(3), legend, sp(10)]
    f.append(box('Economics = study of CHOICE under SCARCITY. Every topic in this note comes from three ideas: '
                 '(1) resources are scarce, (2) choices have opportunity costs, (3) prices (demand and supply) coordinate choices.',
                 ORG, label='BIG IDEA:'))
    f.append(sp(8))
    f.append(sub('TOP 10 THINGS EXAMINERS ALWAYS ASK', RED))
    f += bl(['Definitions of Smith, Marshall, Robbins, Samuelson with <b>criticism</b>',
             'Circular-flow diagram (labelled)', 'PPF graph, opportunity cost, growth shift',
             'Positive vs normative statements with examples', 'Law of demand and law of supply',
             'Shifters of demand and supply with examples', 'Shift vs movement along the curve',
             'Equilibrium numerical (Qd = 50 - 5P, Qs = 5 + 10P)', 'Surplus and shortage with graph',
             '3-step method with combined shifts (ambiguous effect)'], RED)
    return f

# ---- Page 2
def page2():
    f = [hdr('Definitions of Economics', 'Chapter 1 / Introduction', IND, 2), sp(6)]
    data = [['Economist', 'Definition and Focus', 'Criticism'],
            ['<font color="#3F51B5">Adam Smith</font><br/>1776 (Classical)',
             '"Economics is the <b>science of wealth</b>."<br/>Focus: production and accumulation of wealth; how nations grow richer. Called <b>Father of Economics</b> (book: The Wealth of Nations).',
             'Too narrow. Ignores human and social welfare.'],
            ['<font color="#00897B">Alfred Marshall</font><br/>1890 (Neoclassical)',
             '"Economics is the study of mankind in the <b>ordinary business of life</b>."<br/>Focus: human <b>welfare</b>, income, consumption, well-being. A social science.',
             'Limited to material welfare only.'],
            ['<font color="#EF6C00">Lionel Robbins</font><br/>1932 (Scarcity)',
             '"Economics is the science which studies human behavior as a relationship between <b>ends</b> and <b>scarce means</b> which have <b>alternative uses</b>."<br/>Emphasis: scarcity, choice, opportunity cost. Covers material and non-material wants.',
             'Ignores human welfare and ethics.'],
            ['<font color="#7B1FA2">Paul Samuelson</font><br/>Modern',
             '"Study of how people and society choose, <b>with or without money</b>, to employ scarce productive resources..."<br/>Integrates scarcity, choice, efficiency and welfare. Covers micro and macro, future planning and policy.',
             'Considered the <b>most complete</b> definition.'],
            ['<font color="#D32F2F">J. M. Keynes</font><br/>1930s (Macro)',
             '(No direct quote) Focus on <b>employment, income, output and demand</b>. Advocated government intervention. Developed macroeconomics; transformed economics after the Great Depression.',
             'Mainly short-run, macro focus.']]
    f.append(T(data, IND, colw=[100, 280, 120], st=ParagraphStyle('t2', parent=small, fontSize=8.4, leading=11)))
    f.append(sp(8))
    f.append(sub('MEMORY TRICKS', ORG))
    tr = Table([[P('<b><font color="#3F51B5">S</font>mith</b> = <b>W</b>ealth'), P('<b><font color="#00897B">M</font>arshall</b> = <b>W</b>elfare'),
                 P('<b><font color="#EF6C00">R</font>obbins</b> = <b>R</b>arity (Scarcity)'), P('<b><font color="#7B1FA2">S</font>amuelson</b> = Scarce + Social choice')]],
               colWidths=[W / 4] * 4)
    tr.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), light(ORG, 0.9)), ('BOX', (0, 0), (-1, -1), 0.8, ORG),
                            ('INNERGRID', (0, 0), (-1, -1), 0.3, ORG), ('TOPPADDING', (0, 0), (-1, -1), 6), ('BOTTOMPADDING', (0, 0), (-1, -1), 6)]))
    f += [tr, sp(8)]
    f.append(sub('EVOLUTION OF DEFINITIONS (Timeline)', TEAL))
    tl = Table([[P('<b>1776</b><br/>Smith<br/>WEALTH'), P('<b>1890</b><br/>Marshall<br/>WELFARE'), P('<b>1932</b><br/>Robbins<br/>SCARCITY'),
                 P('<b>1930s</b><br/>Keynes<br/>MACRO'), P('<b>Modern</b><br/>Samuelson<br/>COMPLETE')]], colWidths=[W / 5] * 5)
    cols = [IND, TEAL, ORG, RED, PUR]
    st = [('TOPPADDING', (0, 0), (-1, -1), 8), ('BOTTOMPADDING', (0, 0), (-1, -1), 8), ('ALIGN', (0, 0), (-1, -1), 'CENTER')]
    for i, c in enumerate(cols):
        st.append(('BACKGROUND', (i, 0), (i, 0), light(c, 0.82)))
        st.append(('BOX', (i, 0), (i, 0), 1.2, c))
    tl.setStyle(TableStyle(st))
    f += [tl, sp(8)]
    f.append(sub('HOW TO WRITE A 10-MARK ANSWER', PINK))
    f += bl(['<b>Intro:</b> one line - meaning of economics changed over time.',
             '<b>Body:</b> five definitions, each with <b>quote + focus + criticism</b> (use the table above).',
             '<b>Compare:</b> draw a small table (Economist, Focus, Criticism).',
             '<b>Conclusion:</b> Samuelson gives the most complete modern view; Keynes added macroeconomics.'], PINK)
    f.append(sp(6))
    f.append(box('Smith = Wealth (too narrow), Marshall = Welfare (material only), Robbins = Scarcity (ignores ethics), '
                 'Samuelson = with or without money (complete), Keynes = Employment and demand (govt. intervention).', IND, label='ONE-LINE REVISION:'))
    return f

# ---- Page 3
def page3():
    f = [hdr('Core Concepts', 'Scarcity | Opportunity Cost | Micro vs Macro', TEAL, 3), sp(6)]
    left = [sub('SCARCITY', TEAL, W / 2 - 8)] + bl(
        ['<b>Unlimited wants</b> vs <b>limited resources</b>.', 'Root of all economic problems.',
         'Forces every society to <b>choose</b>.', 'Every choice has an opportunity cost.'], TEAL)
    right = [sub('OPPORTUNITY COST', ORG, W / 2 - 8)] + bl(
        ['Value of the <b>next best alternative</b> given up.', 'Includes time, effort and money.',
         'Example: 3 hours study = lost part-time wage.', 'On PPF: slope = opportunity cost.'], ORG)
    f += [two(left, right), sp(6)]
    f.append(sub('FACTORS OF PRODUCTION (Inputs)', IND))
    f.append(sp(3))
    f.append(T([['Factor', 'Meaning', 'Reward', 'Example'],
                ['Land', 'Natural resources', 'Rent', 'Farmland, minerals'],
                ['Labor', 'Human effort', 'Wages', 'Teacher, programmer'],
                ['Capital', 'Man-made tools', 'Interest', 'Machines, computers'],
                ['Entrepreneurship', 'Organizing and risk-taking', 'Profit', 'Business owner']], IND, colw=[110, 150, 100, 140], bold_first_col=True))
    f.append(sp(6))
    f.append(sub('INDIVIDUAL TO GLOBAL (Scale of Economics)', PUR))
    chain = ['Individual', 'Household', 'Family', 'Society', 'Village/Ward', 'Upazila-District-Division', 'Country', 'Continent', 'Global']
    cells = [[P('<font color="white"><b>%s</b></font>' % c, smallc) for c in chain]]
    wd = [48, 52, 42, 46, 58, 92, 48, 56, 42]
    ch = Table(cells, colWidths=wd)
    ps = [PUR, BLU, TEAL, GRN, ORG, RED, PINK, IND, PUR]
    ch.setStyle(TableStyle([('BACKGROUND', (i, 0), (i, 0), ps[i]) for i in range(9)] +
                           [('TOPPADDING', (0, 0), (-1, -1), 6), ('BOTTOMPADDING', (0, 0), (-1, -1), 6), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                            ('LEFTPADDING', (0, 0), (-1, -1), 2), ('RIGHTPADDING', (0, 0), (-1, -1), 2)]))
    f += [sp(3), ch, sp(8)]
    f.append(sub('MICROECONOMICS vs MACROECONOMICS', BLU))
    f.append(sp(3))
    f.append(T([['Basis', 'Microeconomics', 'Macroeconomics'],
                ['Definition', 'How households and firms make decisions and interact in markets', 'Economy-wide phenomena: inflation, unemployment, growth'],
                ['Unit of study', 'Individual consumers, firms, single markets', 'Whole economy (aggregates)'],
                ['Central problem', 'Price determination', 'Income and employment determination'],
                ['Also called', 'Price theory', 'Income theory'],
                ['Tools', 'Demand, supply, cost, market structure', 'GDP, price level, money supply, policy'],
                ['Example', 'Price of rice; a firm output decision', 'National inflation rate; GDP growth of Bangladesh']],
               BLU, colw=[90, 205, 205], bold_first_col=True))
    f.append(sp(6))
    f.append(sub('THREE BASIC ECONOMIC QUESTIONS', RED))
    q = Table([[P('<b>WHAT</b> to produce?<br/>Which goods and how much (cars or computers)'), P('<b>HOW</b> to produce?<br/>Which technique (labor or capital intensive)'),
                P('<b>FOR WHOM</b> to produce?<br/>How output is shared among people')]], colWidths=[W / 3] * 3)
    q.setStyle(TableStyle([('BACKGROUND', (0, 0), (0, 0), light(RED, 0.88)), ('BACKGROUND', (1, 0), (1, 0), light(ORG, 0.88)),
                           ('BACKGROUND', (2, 0), (2, 0), light(GRN, 0.88)), ('INNERGRID', (0, 0), (-1, -1), 1, white),
                           ('TOPPADDING', (0, 0), (-1, -1), 6), ('BOTTOMPADDING', (0, 0), (-1, -1), 6)]))
    f += [sp(3), q, sp(6)]
    f.append(box('Ceteris paribus = "other things equal". We change ONE variable (price) and hold the rest constant. '
                 'If price changes -> movement along the curve. If anything else changes -> the curve shifts.', ORG, label='KEY ASSUMPTION:'))
    return f

# ---- Page 4
def page4():
    f = [hdr('Circular-Flow Diagram', 'Chapter 2 - Models of Economics', ORG, 4), sp(6)]
    f.append(box('A <b>visual model of the economy</b> that shows how dollars flow through markets among households and firms.', ORG, label='DEFINITION:'))
    f += [sp(6), circular_fig(), sp(6)]
    left = [sub('TWO SECTORS', BLU, W / 2 - 8)] + bl(
        ['<b>Households:</b> buy and consume goods and services; own and sell factors of production.',
         '<b>Firms:</b> produce and sell goods and services; hire and use factors of production.'], BLU)
    right = [sub('TWO MARKETS', GRN, W / 2 - 8)] + bl(
        ['<b>Goods and services market:</b> firms sell, households buy.',
         '<b>Factors of production market:</b> households sell (labor, land, capital), firms buy.'], GRN)
    f += [two(left, right), sp(6)]
    f.append(sub('ALL FLOWS AT A GLANCE', PUR))
    f.append(sp(3))
    f.append(T([['Flow', 'From to To', 'Type'],
                ['Spending', 'Households to goods market', 'Money (green)'],
                ['Revenue', 'Goods market to Firms', 'Money (green)'],
                ['Wages, rent, profit', 'Firms to factor market', 'Money (green)'],
                ['Income', 'Factor market to Households', 'Money (green)'],
                ['Goods and services sold / bought', 'Firms to goods market to Households', 'Real (orange)'],
                ['Labor, land, capital / inputs', 'Households to factor market to Firms', 'Real (orange)']],
               PUR, colw=[170, 200, 130], bold_first_col=True))
    f.append(sp(6))
    left = [sub('ADVANTAGES', GRN, W / 2 - 8)] + bl(
        ['Simple way to understand the economy', 'Shows interdependence of households and firms',
         'Shows money and goods move in opposite directions', 'Base for GDP and national income'], GRN)
    right = [sub('DISADVANTAGES', RED, W / 2 - 8)] + bl(
        ['Ignores government and taxes', 'Ignores savings, banks and investment',
         'Ignores foreign trade', 'Assumes all income is spent (unrealistic)'], RED)
    f += [two(left, right), sp(6)]
    f.append(box('One person\'s <b>spending</b> is another person\'s <b>income</b>, so money moves in a circle. '
                 'Orange arrows = goods/services, green arrows = dollars; they run in opposite directions.', ORG, label='REMEMBER:'))
    return f

# ---- Page 5
def page5():
    f = [hdr('Production Possibilities Frontier', 'PPF | Efficiency | Opportunity Cost', RED, 5), sp(6)]
    f.append(box('A graph that shows the <b>combinations of output</b> the economy can possibly produce given the available '
                 '<b>factors of production</b> and the available <b>production technology</b>.', RED, label='DEFINITION:'))
    f.append(sp(6))
    tbl = T([['Point', 'Computers', 'Cars', 'Status'],
             ['(axis)', '0', '1000', 'On frontier'],
             ['A', '2000', '700', 'Efficient'],
             ['C', '2200', '600', 'Efficient'],
             ['(axis)', '3000', '0', 'On frontier'],
             ['B', '1000', '300', '<font color="#D32F2F">Inefficient (inside)</font>'],
             ['D', '?', '?', '<font color="#C2185B">Unattainable (outside)</font>']],
            RED, colw=[40, 62, 45, 100], bold_first_col=True)
    leftc = [tbl, sp(6), sub('WHAT EACH REGION MEANS', GRN, 247)] + bl(
        ['<b>On the PPF (A, C):</b> efficient, resources fully used', '<b>Inside (B):</b> inefficient, resources wasted or unemployed',
         '<b>Outside (D):</b> cannot be produced now', '<b>Slope:</b> downward (producing more of one means less of the other)'], GRN)
    f.append(two(leftc, [ppf_fig()], wl=250, wr=250))
    f.append(sp(6))
    f.append(sub('OPPORTUNITY COST FROM THE PPF', ORG))
    f.append(sp(3))
    f.append(T([['Move', 'Computers gained', 'Cars lost', 'Opportunity cost of 1 computer'],
                ['(0 comp, 1000 cars) to A', '+2000', '-300', '0.15 car'],
                ['A to C', '+200', '-100', '<b>0.50 car</b>  (1 car = 2 computers)'],
                ['C to (3000 comp, 0 cars)', '+800', '-600', '0.75 car']], ORG, colw=[150, 100, 80, 170], bold_first_col=True))
    f.append(sp(5))
    left = [sub('WHY IS THE PPF BOWED OUTWARD?', PUR, W / 2 - 8)] + bl(
        ['Resources are not equally good at making both goods.', 'Law of <b>increasing opportunity cost</b>.',
         'Best-suited resources move first (low cost).', 'Later moves use less suitable resources (higher cost).'], PUR)
    right = [sub('THE PPF SHOWS 5 CONCEPTS', BLU, W / 2 - 8)] + bl(
        ['<b>Scarcity:</b> points outside are unattainable', '<b>Choice:</b> pick a point on the frontier',
         '<b>Opportunity cost:</b> the slope', '<b>Efficiency:</b> points on the frontier', '<b>Growth:</b> shift of the frontier'], BLU)
    f.append(two(left, right))
    f.append(sp(5))
    f.append(box('B (1000 comp, 300 cars) to A (2000 comp, 700 cars) gives <b>+1000 computers AND +400 cars</b> with no sacrifice. '
                 'That is why B is inefficient.', RED, label='EXAM EXAMPLE:'))
    return f

# ---- Page 6
def page6():
    f = [hdr('PPF Shift and Positive vs Normative', 'Growth | Statements', GRN, 6), sp(6)]
    f.append(sub('SHIFT OF THE PPF (Economic Growth)', GRN))
    f.append(sp(4))
    leftc = [P('<b>Before:</b> max computers 3,000, max cars 1,000.<br/><b>Point A:</b> 700 cars, 2,000 computers.', body), sp(4),
             P('<b>After technology improvement:</b> max computers rise to 4,000; max cars stay 1,000.<br/><b>Point E:</b> 750 cars, 2,100 computers.', body), sp(4),
             box('E has MORE cars and MORE computers than A. The economy can now produce more of both goods = <b>growth</b>.', GRN, 245, label='MEANING:'), sp(5)]
    leftc += bl(['<b>Outward shift:</b> better technology, more labor or capital, education, new resources.',
                 '<b>Inward shift:</b> war, natural disaster, resource depletion, economic collapse.'], GRN)
    f.append(two(leftc, [ppf_shift_fig()], wl=250, wr=250))
    f.append(sp(6))
    f.append(T([['Outward shift (growth)', 'Inward shift (decline)'],
                ['Better technology', 'War or natural disaster'], ['More labor or capital', 'Fall in labor or capital'],
                ['Better education and skills', 'Resource depletion'], ['Discovery of resources', 'Economic collapse']],
               GRN, colw=[250, 250]))
    f.append(sp(8))
    f.append(sub('POSITIVE vs NORMATIVE STATEMENTS (Perception vs Reality)', PUR))
    f.append(sp(3))
    f.append(T([['Basis', 'Positive statement', 'Normative statement'],
                ['Meaning', 'Claims that attempt to <b>describe the world as it is</b>', 'Claims that attempt to <b>prescribe how the world should be</b>'],
                ['Nature', 'Factual, objective', 'Opinion, value judgment'],
                ['Proof', 'Can be tested with data (true or false)', 'Cannot be proved true or false'],
                ['Key words', 'is, are, will', 'should, ought, must'],
                ['Example 1', 'Minimum wage laws cause unemployment.', 'The government should raise the minimum wage.'],
                ['Example 2', 'Inflation in Bangladesh was 9% last year.', 'Inflation ought to be below 5%.'],
                ['Branch', 'Positive economics', 'Normative economics']],
               PUR, colw=[70, 215, 215], bold_first_col=True))
    f.append(sp(6))
    f.append(sub('CLASSIFY THESE (Practice)', ORG))
    f.append(sp(3))
    f.append(T([['Statement', 'Type'],
                ['"A rise in the price of tea reduces the quantity of tea demanded."', '<font color="#7B1FA2"><b>Positive</b></font>'],
                ['"The government should provide free textbooks."', '<font color="#C2185B"><b>Normative</b></font>'],
                ['"The unemployment rate is 5 percent."', '<font color="#7B1FA2"><b>Positive</b></font>'],
                ['"Rich people ought to pay higher taxes."', '<font color="#C2185B"><b>Normative</b></font>']],
               ORG, colw=[390, 110]))
    f.append(sp(6))
    f.append(box('If you can <b>test it with data</b>, it is POSITIVE. If it contains <b>opinion or "should"</b>, it is NORMATIVE.', PUR, label='RULE:'))
    return f

# ---- Page 7
def page7():
    f = [hdr('Markets and Demand', 'Chapter 4 - Mankiw', BLU, 7), sp(6)]
    left = [sub('MARKET', BLU, W / 2 - 8)] + bl(
        ['A group of <b>buyers and sellers</b> of a particular good or service.', 'Buyers as a group determine <b>demand</b>.', 'Sellers as a group determine <b>supply</b>.'], BLU)
    right = [sub('COMPETITIVE MARKETS', GRN, W / 2 - 8)] + bl(
        ['<b>Competitive:</b> many buyers and sellers, each has negligible impact on price.',
         '<b>Perfectly competitive:</b> (1) all goods exactly the same, (2) so many buyers/sellers that no one affects price.',
         'Everyone is a <b>price taker</b>.'], GRN)
    f += [two(left, right), sp(6)]
    f.append(sub('DEMAND - KEY DEFINITIONS', RED))
    f += bl(['<b>Quantity demanded (Qd):</b> amount of a good buyers are <b>willing and able</b> to purchase.',
             '<b>Law of demand:</b> other things equal, price up -> Qd down; price down -> Qd up (negative relationship).',
             '<b>Demand schedule:</b> a table of price and quantity demanded. <b>Demand curve:</b> its graph, <b>downward sloping</b>.'], RED)
    f.append(sp(4))
    f.append(sub('SAM\'S DEMAND SCHEDULE (Lattes)', BLU))
    f.append(sp(3))
    ds = T([['Price', '$0', '$1', '$2', '$3', '$4', '$5', '$6'], ['Qty demanded', '16', '14', '12', '10', '8', '6', '4']], BLU,
           colw=[90] + [58] * 7, bold_first_col=True)
    f += [ds, sp(4)]
    f += bl(['Each $1 rise in price lowers quantity by 2 -> <b>Qd = 16 - 2P</b> (choke price = $8).'], BLU)
    # demand curve drawing
    d = Drawing(240, 150)
    ox, oy, pw, ph = 34, 22, 190, 118
    mx = lambda q: ox + q / 18.0 * pw
    my = lambda p: oy + p / 6.5 * ph
    d.add(Line(ox, oy, ox, oy + ph + 4, strokeColor=colors.black))
    d.add(Line(ox, oy, ox + pw + 4, oy, strokeColor=colors.black))
    d.add(Line(mx(16), my(0), mx(3), my(6.5), strokeColor=BLU, strokeWidth=2.4))
    for p, q in [(6, 4), (5, 6), (4, 8), (3, 10), (2, 12), (1, 14), (0, 16)]:
        d.add(Circle(mx(q), my(p), 3, fillColor=BLU, strokeColor=BLU))
        d.add(String(ox - 4, my(p) - 2, '$%d' % p, fontSize=7, textAnchor='end'))
    for q in (0, 5, 10, 15):
        d.add(String(mx(q), oy - 10, str(q), fontSize=7, textAnchor='middle'))
    d.add(String(ox + pw / 2, 2, 'Quantity of Lattes', fontSize=8, textAnchor='middle', fontName='Helvetica-Bold'))
    d.add(String(4, oy + ph + 5, 'Price of Lattes', fontSize=8, fontName='Helvetica-Bold'))
    d.add(String(mx(10) + 4, my(5), 'Sam\'s demand curve', fontSize=8, fillColor=BLU, fontName='Helvetica-Bold'))
    leftc = [sp(4), sub('WHY DOES DEMAND SLOPE DOWNWARD?', PUR, 250)] + bl(
        ['<b>Substitution effect:</b> buyers switch to cheaper substitutes', '<b>Income effect:</b> higher price cuts real purchasing power',
         '<b>Diminishing marginal utility:</b> extra units give less satisfaction', '<b>New buyers</b> enter at lower prices'], PUR)
    f.append(two(leftc, [d], wl=250, wr=250))
    f.append(sp(5))
    f.append(sub('MARKET DEMAND = SUM OF INDIVIDUAL DEMANDS', ORG))
    f.append(sp(3))
    f.append(T([['Price', '$0', '$1', '$2', '$3', '$4', '$5', '$6'],
                ['Sam Qd', '16', '14', '12', '10', '8', '6', '4'], ['Dean Qd', '8', '7', '6', '5', '4', '3', '2'],
                ['<b>Market Qd</b>', '<b>24</b>', '<b>21</b>', '<b>18</b>', '<b>15</b>', '<b>12</b>', '<b>9</b>', '<b>6</b>']],
               ORG, colw=[90] + [58] * 7, bold_first_col=True))
    f.append(sp(4))
    f.append(box('Market demand curve = <b>horizontal sum</b> of individual curves (add QUANTITIES at each price, never prices). '
                 '16-2P + 8-P gives <b>Qd = 24 - 3P</b>.', ORG, label='RULE:'))
    return f

# ---- Page 8
def page8():
    f = [hdr('Demand Curve Shifters', 'Non-price determinants of demand', PINK, 8), sp(6)]
    f.append(box('The demand curve shows how <b>price</b> affects quantity demanded, other things equal. '
                 'The "other things" are the <b>non-price determinants</b>. When they change, the whole curve <b>SHIFTS</b> '
                 '(right = increase in demand, left = decrease).', PINK, label='IDEA:'))
    f.append(sp(5))
    f.append(sub('FIVE SHIFTERS  -  memory aid: I - P - T - E - N', PINK))
    f.append(sp(3))
    f.append(T([['Shifter', 'Change', 'Effect on demand', 'Example'],
                ['<b>I</b>ncome (normal good)', 'Income up', 'D shifts RIGHT', 'Restaurant meals, smartphones'],
                ['<b>I</b>ncome (inferior good)', 'Income up', 'D shifts LEFT', 'Instant noodles, public bus'],
                ['<b>P</b>rice of substitute', 'Price of substitute up', 'D shifts RIGHT', 'Pizza price up, hamburger demand up'],
                ['<b>P</b>rice of complement', 'Price of complement up', 'D shifts LEFT', 'Computer price up, software demand down'],
                ['<b>T</b>astes', 'Tastes move toward good', 'D shifts RIGHT', 'Atkins diet in the 90s raised egg demand'],
                ['<b>E</b>xpectations', 'Expect higher income or prices', 'D shifts RIGHT now', 'Expect pay rise: more restaurant meals now'],
                ['<b>N</b>umber of buyers', 'More buyers', 'D shifts RIGHT', 'Rise by 5 at each price']],
               PINK, colw=[120, 120, 100, 160]))
    f.append(sp(6))
    left = [sub('NUMBER OF BUYERS (Slide Example)', BLU, W / 2 - 8),
            T([['Price', 'Old Qd', 'New Qd'], ['$0', '24', '29'], ['$1', '21', '26'], ['$2', '18', '23'], ['$3', '15', '20'], ['$4', '12', '17'], ['$5', '9', '14'], ['$6', '6', '11']],
              BLU, colw=[60, 90, 90])]
    d = Drawing(240, 150)
    ox, oy, pw, ph = 34, 22, 190, 118
    mx = lambda q: ox + q / 32.0 * pw
    my = lambda p: oy + p / 6.8 * ph
    d.add(Line(ox, oy, ox, oy + ph + 4, strokeColor=colors.black))
    d.add(Line(ox, oy, ox + pw + 4, oy, strokeColor=colors.black))
    d.add(Line(mx(24), my(0), mx(4), my(6.6), strokeColor=BLU, strokeWidth=2.2))
    d.add(Line(mx(29), my(0), mx(9), my(6.6), strokeColor=PINK, strokeWidth=2.2))
    for p in (0, 2, 4, 6):
        d.add(Line(mx(24 - 3 * p + 5 * 0), my(p), mx(29 - 3 * p), my(p), strokeColor=ORG, strokeWidth=1.1))
        d.add(String(ox - 4, my(p) - 2, '$%d' % p, fontSize=7, textAnchor='end'))
    for q in (0, 10, 20, 30):
        d.add(String(mx(q), oy - 10, str(q), fontSize=7, textAnchor='middle'))
    d.add(String(mx(8), my(5.7), 'D1', fontSize=8, fontName='Helvetica-Bold', fillColor=BLU))
    d.add(String(mx(14), my(5.7), 'D2 (more buyers)', fontSize=8, fontName='Helvetica-Bold', fillColor=PINK))
    d.add(String(ox + pw / 2, 2, 'Quantity', fontSize=8, textAnchor='middle', fontName='Helvetica-Bold'))
    d.add(String(4, oy + ph + 5, 'Price', fontSize=8, fontName='Helvetica-Bold'))
    f.append(two(left, [d], wl=250, wr=250))
    f.append(sp(6))
    f.append(sub('SUMMARY: VARIABLES THAT INFLUENCE BUYERS', TEAL))
    f.append(sp(3))
    f.append(T([['Variable', 'A change in this variable...'],
                ['Price of the good itself', '<font color="#D32F2F"><b>MOVEMENT ALONG</b></font> the demand curve'],
                ['Income, related goods, tastes, expectations, number of buyers', '<font color="#2E7D32"><b>SHIFTS</b></font> the demand curve']],
               TEAL, colw=[250, 250]))
    f.append(sp(5))
    f.append(box('<b>Normal good:</b> income up -> demand up.  <b>Inferior good:</b> income up -> demand down.  '
                 '<b>Substitutes:</b> same direction.  <b>Complements:</b> opposite direction.', PINK, label='QUICK RULES:'))
    return f

# ---- Page 9
def page9():
    f = [hdr('Related Goods and Active Learning 1', 'Substitutes | Complements | Shift vs Movement', TEAL, 9), sp(6)]
    left = [sub('SUBSTITUTES', ORG, W / 2 - 8)] + bl(
        ['Price of one up -> demand for the other <b>UP</b>.', 'Used instead of each other.',
         '<b>Example:</b> pizza and hamburgers (pizza price up -> hamburger D shifts right).', 'Others: Coke and Pepsi, laptops and tablets, music CDs and downloads.'], ORG)
    right = [sub('COMPLEMENTS', BLU, W / 2 - 8)] + bl(
        ['Price of one up -> demand for the other <b>DOWN</b>.', 'Used together.',
         '<b>Example:</b> computers and software (computer price up -> software D shifts left).', 'Others: tuition and textbooks, bagels and cream cheese, eggs and bacon.'], BLU)
    f += [two(left, right), sp(6)]
    f.append(T([['Basis', 'Substitutes', 'Complements'],
                ['Price of A rises', 'Demand for B rises', 'Demand for B falls'], ['Cross effect', 'Positive', 'Negative'],
                ['Example', 'Coke - Pepsi', 'Car - petrol']], TEAL, colw=[120, 190, 190], bold_first_col=True))
    f.append(sp(8))
    f.append(sub('ACTIVE LEARNING 1: Demand for MUSIC DOWNLOADS', PUR))
    f.append(sp(3))
    f.append(T([['Scenario', 'Reasoning', 'Result'],
                ['A. Price of iPods falls', 'iPods and downloads are <b>complements</b>', '<font color="#2E7D32"><b>D shifts RIGHT</b></font>'],
                ['B. Price of music downloads falls', 'Own price changed', '<font color="#D32F2F"><b>NO shift</b></font>; move DOWN along D (lower P, higher Q)'],
                ['C. Price of music CDs falls', 'CDs and downloads are <b>substitutes</b>', '<font color="#2E7D32"><b>D shifts LEFT</b></font>']],
               PUR, colw=[150, 170, 180], bold_first_col=True))
    f.append(sp(6))
    # three mini panels
    pa = shift_panel('A: iPod price falls', 0.2, 0, 'P up', 'Q up', GRN)
    pb = Drawing(118, 118)
    ox, oy, pw, ph = 8, 18, 100, 78
    pb.add(Rect(0, 0, 118, 118, fillColor=light(RED, 0.93), strokeColor=RED, strokeWidth=0.8, rx=5, ry=5))
    pb.add(Line(ox, oy, ox, oy + ph, strokeColor=colors.black, strokeWidth=0.8))
    pb.add(Line(ox, oy, ox + pw, oy, strokeColor=colors.black, strokeWidth=0.8))
    pb.add(Line(ox + 0.1 * pw, oy + 0.82 * ph, ox + 0.9 * pw, oy + 0.18 * ph, strokeColor=BLU, strokeWidth=2))
    pb.add(Circle(ox + 0.35 * pw, oy + 0.62 * ph, 3, fillColor=GRN, strokeColor=GRN))
    pb.add(Circle(ox + 0.65 * pw, oy + 0.38 * ph, 3, fillColor=RED, strokeColor=RED))
    arrow(pb, [(ox + 0.35 * pw + 3, oy + 0.62 * ph - 3), (ox + 0.65 * pw - 3, oy + 0.38 * ph + 3)], RED, 1.2)
    pb.add(String(59, 107, 'B: own price falls', fontSize=7.8, fontName='Helvetica-Bold', textAnchor='middle', fillColor=RED))
    pb.add(String(59, 6, 'MOVEMENT along D', fontSize=7, fontName='Helvetica-Bold', textAnchor='middle'))
    pc = shift_panel('C: CD price falls', -0.2, 0, 'P down', 'Q down', ORG)
    panels = Table([[pa, pb, pc]], colWidths=[W / 3] * 3)
    panels.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('LEFTPADDING', (0, 0), (-1, -1), 0), ('RIGHTPADDING', (0, 0), (-1, -1), 0)]))
    f += [panels, sp(8)]
    f.append(sub('CHANGE IN DEMAND vs CHANGE IN QUANTITY DEMANDED', RED))
    f.append(sp(3))
    f.append(T([['Basis', 'Change in DEMAND', 'Change in QUANTITY DEMANDED'],
                ['Cause', 'Non-price determinant (income, tastes, buyers, related goods, expectations)', 'Change in the good\'s <b>own price</b>'],
                ['Graph', 'Whole curve <b>SHIFTS</b>', '<b>MOVEMENT ALONG</b> a fixed curve'],
                ['Words', 'Increase / decrease in demand', 'Expansion / contraction of quantity demanded']],
               RED, colw=[70, 230, 200], bold_first_col=True))
    f.append(sp(5))
    f.append(box('<b>Own price changes = move along the curve. ANYTHING else changes = shift the curve.</b>', RED, label='GOLDEN RULE:'))
    return f

# ---- Page 10
def page10():
    f = [hdr('Supply', 'Law of Supply | Market Supply', ORG, 10), sp(6)]
    f.append(sub('SUPPLY - KEY DEFINITIONS', ORG))
    f += bl(['<b>Quantity supplied (Qs):</b> amount of a good sellers are <b>willing and able</b> to sell.',
             '<b>Law of supply:</b> other things equal, price up -> Qs up; price down -> Qs down (positive relationship).',
             '<b>Supply schedule:</b> table of price and quantity supplied. <b>Supply curve:</b> its graph, <b>upward sloping</b>.'], ORG)
    f.append(sp(4))
    f.append(sub('STARBUCKS\' SUPPLY SCHEDULE (Lattes)', RED))
    f.append(sp(3))
    f.append(T([['Price', '$0', '$1', '$2', '$3', '$4', '$5', '$6'], ['Qty supplied', '0', '3', '6', '9', '12', '15', '18']], RED,
               colw=[90] + [58] * 7, bold_first_col=True))
    f.append(sp(3))
    f += bl(['Each $1 rise in price adds 3 lattes -> <b>Qs = 3P</b>.'], RED)
    d = Drawing(240, 150)
    ox, oy, pw, ph = 34, 22, 190, 118
    mx = lambda q: ox + q / 20.0 * pw
    my = lambda p: oy + p / 6.5 * ph
    d.add(Line(ox, oy, ox, oy + ph + 4, strokeColor=colors.black))
    d.add(Line(ox, oy, ox + pw + 4, oy, strokeColor=colors.black))
    d.add(Line(mx(0), my(0), mx(19.5), my(6.5), strokeColor=RED, strokeWidth=2.4))
    for p in range(0, 7):
        d.add(Circle(mx(3 * p), my(p), 3, fillColor=RED, strokeColor=RED))
        d.add(String(ox - 4, my(p) - 2, '$%d' % p, fontSize=7, textAnchor='end'))
    for q in (0, 5, 10, 15):
        d.add(String(mx(q), oy - 10, str(q), fontSize=7, textAnchor='middle'))
    d.add(String(ox + pw / 2, 2, 'Quantity of Lattes', fontSize=8, textAnchor='middle', fontName='Helvetica-Bold'))
    d.add(String(4, oy + ph + 5, 'Price of Lattes', fontSize=8, fontName='Helvetica-Bold'))
    d.add(String(mx(9), my(1), 'Starbucks supply curve', fontSize=8, fillColor=RED, fontName='Helvetica-Bold'))
    leftc = [sp(4), sub('WHY DOES SUPPLY SLOPE UPWARD?', PUR, 250)] + bl(
        ['<b>Profit motive:</b> higher price = more profit per unit', '<b>Rising marginal cost:</b> more output costs more per unit',
         '<b>New sellers</b> are attracted by high price', '<b>Existing firms</b> expand production'], PUR)
    f.append(two(leftc, [d], wl=250, wr=250))
    f.append(sp(5))
    f.append(sub('MARKET SUPPLY = SUM OF INDIVIDUAL SUPPLIES', BLU))
    f.append(sp(3))
    f.append(T([['Price', '$0', '$1', '$2', '$3', '$4', '$5', '$6'],
                ['Starbucks Qs', '0', '3', '6', '9', '12', '15', '18'], ['Peet\'s Qs', '0', '2', '4', '6', '8', '10', '12'],
                ['<b>Market Qs</b>', '<b>0</b>', '<b>5</b>', '<b>10</b>', '<b>15</b>', '<b>20</b>', '<b>25</b>', '<b>30</b>']],
               BLU, colw=[90] + [58] * 7, bold_first_col=True))
    f.append(sp(4))
    f.append(box('Market supply = <b>horizontal sum</b> of individual supply curves. 3P + 2P gives <b>Qs = 5P</b>.', BLU, label='RULE:'))
    f.append(sp(6))
    f.append(sub('DEMAND vs SUPPLY - MASTER COMPARISON', GRN))
    f.append(sp(3))
    f.append(T([['Basis', 'Demand', 'Supply'],
                ['Who', 'Buyers', 'Sellers'], ['Law', 'Price up, Qd down', 'Price up, Qs up'], ['Slope', 'Downward', 'Upward'],
                ['Shifters (memory)', 'I-P-T-E-N', 'I-T-E-N'], ['Function', 'Qd = a - bP', 'Qs = c + dP'],
                ['Example', 'Sam\'s lattes', 'Starbucks\' lattes']], GRN, colw=[120, 190, 190], bold_first_col=True))
    return f

# ---- Page 11
def page11():
    f = [hdr('Supply Curve Shifters', 'Non-price determinants of supply', RED, 11), sp(6)]
    f.append(box('The supply curve shows how <b>price</b> affects quantity supplied, other things equal. '
                 'The "other things" are <b>non-price determinants of supply</b>. When they change, the curve <b>SHIFTS</b>.', RED, label='IDEA:'))
    f.append(sp(5))
    f.append(sub('FOUR SHIFTERS  -  memory aid: I - T - E - N', RED))
    f.append(sp(3))
    f.append(T([['Shifter', 'Change', 'Effect on supply', 'Example'],
                ['<b>I</b>nput prices', 'Input price falls (supply is negatively related to input price)', 'S shifts RIGHT', 'Price of milk falls: more lattes (+5 at each price)'],
                ['<b>T</b>echnology', 'Cost-saving technology', 'S shifts RIGHT', 'New technology cuts hybrid car cost'],
                ['<b>E</b>xpectations', 'Expect higher future price (non-perishable)', 'S shifts LEFT now', 'Texas oil owners hold back inventory'],
                ['<b>N</b>umber of sellers', 'More sellers', 'S shifts RIGHT', 'New firms enter the market']],
               RED, colw=[90, 170, 90, 150]))
    f.append(sp(6))
    # input price example table + chart
    left = [sub('INPUT PRICE FALLS (Slide Example)', BLU, W / 2 - 8),
            T([['Price', 'Old Qs', 'New Qs'], ['$1', '5', '10'], ['$2', '10', '15'], ['$3', '15', '20'], ['$4', '20', '25'], ['$5', '25', '30'], ['$6', '30', '35']],
              BLU, colw=[60, 90, 90])]
    d = Drawing(240, 150)
    ox, oy, pw, ph = 34, 22, 190, 118
    mx = lambda q: ox + q / 40.0 * pw
    my = lambda p: oy + p / 6.8 * ph
    d.add(Line(ox, oy, ox, oy + ph + 4, strokeColor=colors.black))
    d.add(Line(ox, oy, ox + pw + 4, oy, strokeColor=colors.black))
    d.add(Line(mx(0), my(0), mx(30.5), my(6.1), strokeColor=RED, strokeWidth=2.2))
    d.add(Line(mx(5), my(0), mx(35.5), my(6.1), strokeColor=GRN, strokeWidth=2.2))
    for p in (1, 2, 3, 4, 5, 6):
        d.add(Line(mx(5 * p), my(p), mx(5 * p + 5), my(p), strokeColor=ORG, strokeWidth=1.1))
        d.add(String(ox - 4, my(p) - 2, '$%d' % p, fontSize=7, textAnchor='end'))
    for q in (0, 10, 20, 30):
        d.add(String(mx(q), oy - 10, str(q), fontSize=7, textAnchor='middle'))
    d.add(String(mx(24), my(2.2), 'S1', fontSize=8, fontName='Helvetica-Bold', fillColor=RED))
    d.add(String(mx(30), my(2.2), 'S2 (cost falls)', fontSize=8, fontName='Helvetica-Bold', fillColor=GRN))
    d.add(String(ox + pw / 2, 2, 'Quantity', fontSize=8, textAnchor='middle', fontName='Helvetica-Bold'))
    d.add(String(4, oy + ph + 5, 'Price', fontSize=8, fontName='Helvetica-Bold'))
    f.append(two(left, [d], wl=250, wr=250))
    f.append(sp(6))
    f.append(sub('SUMMARY: VARIABLES THAT INFLUENCE SELLERS', TEAL))
    f.append(sp(3))
    f.append(T([['Variable', 'A change in this variable...'],
                ['Price of the good itself', '<font color="#D32F2F"><b>MOVEMENT ALONG</b></font> the supply curve'],
                ['Input prices, technology, expectations, number of sellers', '<font color="#2E7D32"><b>SHIFTS</b></font> the supply curve']],
               TEAL, colw=[250, 250]))
    f.append(sp(7))
    f.append(sub('ACTIVE LEARNING 2: Supply of TAX RETURN SOFTWARE', PUR))
    f.append(sp(3))
    f.append(T([['Scenario', 'Reasoning', 'Result'],
                ['A. Retailers cut the price of the software', 'Own price changed', '<font color="#D32F2F"><b>NO shift</b></font>; move DOWN along S (lower P, lower Q)'],
                ['B. Technological advance lowers cost', 'Technology improves', '<font color="#2E7D32"><b>S shifts RIGHT</b></font> (more Q at each price)'],
                ['C. Professional preparers raise their price', '<b>Trick question!</b> Preparers are a substitute for the software', 'Shifts <b>DEMAND</b> (right), <b>not</b> supply']],
               PUR, colw=[170, 150, 180], bold_first_col=True))
    f.append(sp(5))
    f.append(box('<b>Change in supply</b> = shift of S (non-price cause). <b>Change in quantity supplied</b> = movement along a fixed S (price changes).', RED, label='REMEMBER:'))
    return f

# ---- Page 12
def page12():
    f = [hdr('Equilibrium, Surplus and Shortage', 'Supply and Demand Together', GRN, 12), sp(6)]
    left = [sub('EQUILIBRIUM', GRN, 250)] + bl(
        ['<b>Equilibrium:</b> price has reached the level where quantity supplied = quantity demanded.',
         '<b>Equilibrium price:</b> price where Qs = Qd (market-clearing price).', '<b>Equilibrium quantity:</b> Q supplied and demanded at that price.',
         '<b>Lattes:</b> P = <b>$3</b>, Q = <b>15</b>.'], GRN)
    f.append(two(left, [sd_fig()], wl=250, wr=250))
    f.append(sp(4))
    f.append(T([['P', '$0', '$1', '$2', '<font color="#FFFFFF">$3 (E)</font>', '$4', '$5', '$6'],
                ['Qd', '24', '21', '18', '<b>15</b>', '12', '9', '6'],
                ['Qs', '0', '5', '10', '<b>15</b>', '20', '25', '30'],
                ['Result', 'Shortage 24', 'Shortage 16', 'Shortage 8', '<b>Equilibrium</b>', 'Surplus 8', 'Surplus 16', 'Surplus 24']],
               GRN, colw=[48] + [64] * 7, bold_first_col=True))
    f.append(sp(7))
    left = [sub('SURPLUS (Excess Supply)', ORG, W / 2 - 8)] + bl(
        ['<b>Qs &gt; Qd</b>, price <b>above</b> equilibrium.', 'Example: P = $5, Qd = 9, Qs = 25 -> <b>surplus = 16</b>.',
         '<b>Adjustment:</b> sellers have unsold stock -> cut price -> Qd rises, Qs falls -> price falls until equilibrium.'], ORG)
    right = [sub('SHORTAGE (Excess Demand)', PUR, W / 2 - 8)] + bl(
        ['<b>Qd &gt; Qs</b>, price <b>below</b> equilibrium.', 'Example: P = $1, Qd = 21, Qs = 5 -> <b>shortage = 16</b>.',
         '<b>Adjustment:</b> buyers cannot get goods -> sellers raise price -> Qd falls, Qs rises -> price rises until equilibrium.'], PUR)
    f += [two(left, right), sp(6)]
    f.append(T([['Basis', 'Surplus', 'Shortage'],
                ['Also called', 'Excess supply', 'Excess demand'], ['Condition', 'Qs &gt; Qd', 'Qd &gt; Qs'],
                ['Price level', 'Above equilibrium', 'Below equilibrium'], ['Pressure on price', 'Downward', 'Upward'],
                ['Example (slides)', 'P = $5: surplus 16', 'P = $1: shortage 16']], BLU, colw=[130, 185, 185], bold_first_col=True))
    f.append(sp(7))
    f.append(sub('HOW PRICES ALLOCATE RESOURCES', TEAL))
    f += bl(['"Markets are usually a good way to organize economic activity."', 'In market economies, prices adjust to balance supply and demand.',
             'Equilibrium prices are <b>signals</b> that guide economic decisions and allocate scarce resources.',
             'Equilibrium is <b>stable</b>: any deviation triggers forces that restore it.'], TEAL)
    f.append(sp(5))
    f.append(box('Price above E -> SURPLUS -> price falls.  Price below E -> SHORTAGE -> price rises.  Markets self-correct until <b>Qs = Qd</b>.', GRN, label='REMEMBER:'))
    return f

# ---- Page 13
def page13():
    f = [hdr('The 3-Step Method and Shifts', 'Comparative statics', PUR, 13), sp(6)]
    steps = Table([[P('<font color="white"><b>STEP 1</b></font><br/><font color="white">Decide which curve shifts: supply, demand, or both</font>', small),
                    P('<font color="white"><b>STEP 2</b></font><br/><font color="white">Decide the direction: RIGHT or LEFT</font>', small),
                    P('<font color="white"><b>STEP 3</b></font><br/><font color="white">Compare old and new equilibrium: effect on P and Q</font>', small)]],
                  colWidths=[W / 3] * 3)
    steps.setStyle(TableStyle([('BACKGROUND', (0, 0), (0, 0), IND), ('BACKGROUND', (1, 0), (1, 0), PUR), ('BACKGROUND', (2, 0), (2, 0), PINK),
                               ('INNERGRID', (0, 0), (-1, -1), 2, white), ('TOPPADDING', (0, 0), (-1, -1), 7), ('BOTTOMPADDING', (0, 0), (-1, -1), 7)]))
    f += [steps, sp(7)]
    f.append(sub('FOUR BASIC SHIFTS (grey dot = old E, coloured dot = new E)', PUR))
    f.append(sp(3))
    panels = Table([[shift_panel('Demand UP', 0.2, 0, 'P up', 'Q up', BLU), shift_panel('Demand DOWN', -0.2, 0, 'P down', 'Q down', TEAL),
                     shift_panel('Supply UP', 0, 0.2, 'P down', 'Q up', RED), shift_panel('Supply DOWN', 0, -0.2, 'P up', 'Q down', ORG)]],
                   colWidths=[W / 4] * 4)
    panels.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('LEFTPADDING', (0, 0), (-1, -1), 0), ('RIGHTPADDING', (0, 0), (-1, -1), 0)]))
    f += [panels, sp(6)]
    f.append(sub('MASTER TABLE: EFFECT ON EQUILIBRIUM', IND))
    f.append(sp(3))
    f.append(T([['Event', 'Curve shift', 'Price (P)', 'Quantity (Q)'],
                ['Demand increases', 'D right', 'Rises', 'Rises'], ['Demand decreases', 'D left', 'Falls', 'Falls'],
                ['Supply increases', 'S right', 'Falls', 'Rises'], ['Supply decreases', 'S left', 'Rises', 'Falls'],
                ['D right AND S right', 'Both right', '<font color="#D32F2F"><b>Ambiguous</b></font>', 'Rises'],
                ['D left AND S left', 'Both left', '<font color="#D32F2F"><b>Ambiguous</b></font>', 'Falls'],
                ['D right AND S left', 'D right, S left', 'Rises', '<font color="#D32F2F"><b>Ambiguous</b></font>'],
                ['D left AND S right', 'D left, S right', 'Falls', '<font color="#D32F2F"><b>Ambiguous</b></font>']],
               IND, colw=[150, 120, 115, 115], bold_first_col=True))
    f.append(sp(6))
    left = [sub('EXAMPLE 2: Shift in SUPPLY', RED, W / 2 - 8)] + bl(
        ['<b>Event:</b> new technology reduces the cost of producing hybrid cars.', '<b>Step 1:</b> S shifts (cost of production). D does not shift.',
         '<b>Step 2:</b> S shifts <b>RIGHT</b>.', '<b>Step 3:</b> price <b>falls</b>, quantity <b>rises</b>.'], RED)
    right = [sub('EXAMPLE 3: BOTH shift', BLU, W / 2 - 8)] + bl(
        ['<b>Events:</b> gas price rises AND new technology cuts costs.', '<b>Steps 1-2:</b> both curves shift RIGHT.',
         '<b>Step 3:</b> Q <b>rises</b>; P <b>ambiguous</b>.', 'If D rises more -> P rises. If S rises more -> P falls.'], BLU)
    f += [two(left, right), sp(6)]
    f.append(sub('ACTIVE LEARNING 3: Music Downloads Market', ORG))
    f.append(sp(3))
    f.append(T([['Event', 'Step 1', 'Step 2', 'Step 3 (Result)'],
                ['A. Price of music CDs falls', 'D shifts (substitutes)', 'D LEFT', 'P falls, Q falls'],
                ['B. Royalties (cost) fall', 'S shifts (cost)', 'S RIGHT', 'P falls, Q rises'],
                ['C. Both A and B', 'Both shift', 'D left, S right', '<b>P falls</b>; Q is <font color="#D32F2F"><b>ambiguous</b></font> (demand fall lowers Q, supply rise raises Q)']],
               ORG, colw=[130, 110, 80, 180], bold_first_col=True))
    f.append(sp(5))
    f.append(box('Both curves shift -> ONE of P or Q is certain, the OTHER is <b>ambiguous</b>. Always say which shift is bigger decides it.', PUR, label='KEY RULE:'))
    return f

# ---- Page 14
def page14():
    f = [hdr('Maths Problems and Surplus', 'Solved numericals | CS and PS', BLU, 14), sp(6)]
    f.append(sub('1. EQUILIBRIUM (Lecture Problem)', BLU))
    f.append(sp(3))
    eq = [P('<b>Given:</b> Qd = 50 - 5P and Qs = 5 + 10P', body), P('<b>Set Qd = Qs:</b> 50 - 5P = 5 + 10P', body),
          P('45 = 15P  so  <font color="#2E7D32"><b>P = 3</b></font>', body), P('Q = 50 - 5(3) = <font color="#2E7D32"><b>35</b></font>  (check: 5 + 30 = 35)', body)]
    eq2 = [P('<b>Surplus at P = 5:</b> Qd = 25, Qs = 55 -> <font color="#D32F2F"><b>surplus 30</b></font>', body),
           P('<b>Shortage at P = 1:</b> Qd = 45, Qs = 15 -> <font color="#7B1FA2"><b>shortage 30</b></font>', body),
           P('<b>Ceiling at P = 2 (binding):</b> Qd = 40, Qs = 25 -> shortage 15', body),
           P('<b>Floor at P = 4 (binding):</b> Qd = 30, Qs = 45 -> surplus 15', body)]
    f.append(two(eq, eq2))
    f.append(sp(6))
    f.append(sub('2. SHIFTS AND OTHER PROBLEMS', PINK))
    f.append(sp(3))
    f.append(T([['Problem', 'Working', 'Answer'],
                ['Demand rises to Qd = 65 - 5P (Qs = 5 + 10P)', '65 - 5P = 5 + 10P -> 60 = 15P', '<b>P = 4, Q = 45</b> (both rise)'],
                ['Supply rises to Qs = 20 + 10P (Qd = 50 - 5P)', '50 - 5P = 20 + 10P -> 30 = 15P', '<b>P = 2, Q = 40</b> (P falls, Q rises)'],
                ['Qd = 100 - 2P, Qs = 20 + 3P', '80 = 5P', '<b>P = 16, Q = 68</b>'],
                ['Market demand: Sam 16 - 2P, Dean 8 - P', 'Add constants and P terms', '<b>Qd = 24 - 3P</b>'],
                ['Market supply: Starbucks 3P, Peet\'s 2P', '3P + 2P', '<b>Qs = 5P</b>'],
                ['Lattes market: 24 - 3P = 5P', '24 = 8P', '<b>P = 3, Q = 15</b>'],
                ['PPF: A to C (+200 comp, -100 cars)', '100 / 200', '<b>1 computer = 0.5 car</b>']],
               PINK, colw=[190, 160, 150]))
    f.append(sp(7))
    f.append(sub('3. CONSUMER SURPLUS and PRODUCER SURPLUS (Extra Topic)', GRN))
    f.append(sp(3))
    left = bl(['<b>Willingness to pay (WTP):</b> max price a buyer will pay.', '<b>Cost:</b> min price a seller will accept.',
               '<b>Consumer surplus (CS)</b> = WTP - price paid (area below D, above P).', '<b>Producer surplus (PS)</b> = price received - cost (area above S, below P).',
               '<b>Total surplus</b> = CS + PS; <b>maximum at equilibrium</b> (efficient).', '<b>Deadweight loss</b> = fall in total surplus from a distortion.'], GRN)
    right = [T([['Buyer', 'WTP', 'CS at $5'], ['Anna', '$10', '5'], ['Ben', '$8', '3'], ['Chris', '$6', '1'], ['<b>Total CS</b>', '', '<b>9</b>']], GRN, colw=[70, 60, 100]),
             sp(3),
             T([['Seller', 'Cost', 'PS at $5'], ['Seller 1', '$2', '3'], ['Seller 2', '$4', '1'], ['Seller 3', '$5', '0'], ['<b>Total PS</b>', '', '<b>4</b>']], ORG, colw=[70, 60, 100])]
    f.append(two(left, right, wl=262, wr=232))
    f.append(sp(4))
    f.append(box('Total surplus = 9 + 4 = <b>13</b> = (10 + 8 + 6) - (2 + 4 + 5) = 24 - 11. Dina (WTP $4) and Seller 4 (cost $7) do not trade.', GRN, label='CHECK:'))
    f.append(sp(5))
    f.append(T([['Lattes market (Qd = 24 - 3P, Qs = 5P, E: P = 3, Q = 15)', 'Calculation', 'Value'],
                ['Consumer surplus', '1/2 x 15 x (8 - 3)', '<b>37.5</b>'], ['Producer surplus', '1/2 x 15 x (3 - 0)', '<b>22.5</b>'],
                ['Total surplus', '37.5 + 22.5', '<b>60</b>']], GRN, colw=[260, 150, 90]))
    f.append(sp(5))
    f.append(box('<b>Formulas:</b> Equilibrium: Qd = Qs.  Surplus = Qs - Qd (price above E).  Shortage = Qd - Qs (price below E).  '
                 'Opportunity cost of X = (Y given up) / (X gained).  CS (linear) = 1/2 x Q x (choke price - P).', BLU, label=''))
    return f

# ---- Page 15
def page15():
    f = [hdr('Price Controls, Systems, Exceptions', 'Extra topics + final cheat sheet', IND, 15), sp(6)]
    f.append(sub('PRICE CONTROLS (Extra Topic)', RED))
    f.append(sp(3))
    f.append(T([['Basis', 'Price CEILING', 'Price FLOOR'],
                ['Meaning', 'Legal <b>maximum</b> price', 'Legal <b>minimum</b> price'], ['Binding if set', 'BELOW equilibrium', 'ABOVE equilibrium'],
                ['Result', '<font color="#7B1FA2"><b>SHORTAGE</b></font> (queues, black markets)', '<font color="#EF6C00"><b>SURPLUS</b></font> (unsold goods, unemployment)'],
                ['Example', 'Rent control, food price caps', 'Minimum wage, farm support price'],
                ['Lattes example', 'Ceiling $2: Qd 18, Qs 10, shortage 8, DWL 6.67', 'Floor $4: Qd 12, Qs 20, surplus 8, DWL 2.4']],
               RED, colw=[90, 205, 205], bold_first_col=True))
    f.append(sp(6))
    f.append(sub('ECONOMIC SYSTEMS (Extra Topic)', TEAL))
    f.append(sp(3))
    f.append(T([['System', 'Who decides', 'Plus', 'Minus', 'Example'],
                ['Market', 'Prices and private firms', 'Efficiency, innovation', 'Inequality', 'USA'],
                ['Command', 'Government planners', 'Equality, basic needs', 'Inefficiency, no choice', 'North Korea'],
                ['Mixed', 'Market + government', 'Balance of both', 'Govt. inefficiency', 'Bangladesh, India, UK'],
                ['Traditional', 'Custom and habit', 'Stable, simple', 'No growth', 'Tribal groups']],
               TEAL, colw=[70, 110, 110, 110, 100], bold_first_col=True))
    f.append(sp(6))
    left = [sub('EXCEPTIONS TO LAW OF DEMAND', PUR, W / 2 - 8)] + bl(
        ['<b>Giffen good:</b> staple inferior good; price up -> demand up (income effect &gt; substitution effect). Example: potatoes in Irish famine.',
         '<b>Veblen good:</b> luxury status good (diamonds, supercars).', '<b>Expected price rise</b> or speculative goods (shares, gold).',
         '<b>Price as quality signal</b> when buyers cannot judge quality.'], PUR)
    right = [sub('EXCEPTIONS TO LAW OF SUPPLY', ORG, W / 2 - 8)] + bl(
        ['<b>Perishable goods</b> (fish, milk): must sell at any price.', '<b>Fixed or rare supply</b> (antiques, land): vertical curve.',
         '<b>Backward-bending labor supply:</b> at very high wages, workers choose more leisure.', '<b>Expectation</b> of higher future prices: sellers hold back.'], ORG)
    f += [two(left, right), sp(6)]
    f.append(sub('FINAL CHEAT SHEET: DIRECTION OF SHIFTS', GRN))
    f.append(sp(3))
    f.append(T([['DEMAND shifts RIGHT when...', 'SUPPLY shifts RIGHT when...'],
                ['More buyers | Income up (normal good) | Substitute price up | Complement price down | Tastes favour good | Expect higher future income or prices',
                 'Input prices fall | Technology improves | More sellers | (Expect LOWER future price: sellers sell now)']],
               GRN, colw=[250, 250]))
    f.append(sp(5))
    f.append(T([['Term', 'Quick definition'],
                ['Positive / Normative', 'What IS (testable) / what SHOULD BE (opinion)'],
                ['Law of demand / supply', 'Price up: Qd down / Qs up (other things equal)'],
                ['Equilibrium', 'Qs = Qd; surplus above, shortage below'],
                ['Shift vs movement', 'Own price = movement along; other factors = shift']],
               IND, colw=[150, 350], bold_first_col=True))
    f.append(sp(6))
    box_t = Table([[Paragraph('<font color="white" size="14"><b>BEST OF LUCK FOR YOUR EXAM!</b></font><br/>'
                              '<font color="white" size="9">Draw every graph, label every axis, mention "other things equal", and show the 3 steps.</font>',
                              ParagraphStyle('bx', parent=body, alignment=TA_CENTER, leading=18))]], colWidths=[W])
    box_t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), IND), ('TOPPADDING', (0, 0), (-1, -1), 8), ('BOTTOMPADDING', (0, 0), (-1, -1), 8)]))
    f.append(box_t)
    return f

builders = [page1, page2, page3, page4, page5, page6, page7, page8, page9, page10, page11, page12, page13, page14, page15]

def on_page(canvas, doc):
    n = doc.page
    c = PAGE_COLORS[n - 1] if n <= 15 else IND
    canvas.saveState()
    canvas.setFillColor(c)
    canvas.rect(0, A4[1] - 10, A4[0], 10, fill=1, stroke=0)
    canvas.rect(0, 0, A4[0], 22, fill=1, stroke=0)
    canvas.setFillColor(white)
    canvas.setFont('Helvetica-Bold', 8)
    canvas.drawString(40, 8, 'ECONOMICS REVISION NOTE | BRUR CSE')
    canvas.drawRightString(A4[0] - 40, 8, 'Page %d of 15' % n)
    canvas.restoreState()

doc = SimpleDocTemplate('Economics_Revision_15pages.pdf', pagesize=A4, leftMargin=1.4 * cm, rightMargin=1.4 * cm,
                        topMargin=0.9 * cm, bottomMargin=1.0 * cm, title='Economics Revision Note (15 Pages)', author='Revision Note')
avail_w = doc.width - 12
avail_h = doc.height - 12
story = []
for i, b in enumerate(builders):
    content = b()
    story.append(KeepInFrame(avail_w, avail_h - 2, content, mode='shrink'))
    if i < len(builders) - 1:
        story.append(PageBreak())
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print('built')