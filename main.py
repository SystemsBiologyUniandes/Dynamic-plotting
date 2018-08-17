import pandas as pd
from os.path import dirname, join
from bokeh.layouts import row, widgetbox, column
from bokeh.models import Select, Div
from bokeh.models import TextInput
from bokeh.palettes import Spectral5, Viridis9
from bokeh.plotting import curdoc, figure
from bokeh.core.properties import value

desc = Div(text=open(join(dirname(__file__), "description.html")).read(), width=800)

df = pd.read_csv(r'/Users/annypan/Desktop/Cnalyzer/data.csv')
df
df = df.dropna()

df['cv2FSC-A'] = (df['sFSC-A']/df['FSC-A'])**2   
df['cv2SSC-A'] = (df['sSSC-A']/df['SSC-A'])**2   
df['cv2FL1-A'] = (df['sFL1-A']/df['FL1-A'])**2   
df['cv2FL3-A'] = (df['sFL3-A']/df['FL3-A'])**2   
df['cv2FSC-H'] = (df['sFSC-H']/df['FSC-H'])**2   
df['cv2SSC-H'] = (df['sSSC-H']/df['SSC-H'])**2   
df['cv2FL1-H'] = (df['sFL1-H']/df['FL1-H'])**2   
df['cv2FL3-H'] = (df['sFL3-H']/df['FL3-H'])**2   
df['cv2Width'] = (df['sWidth']/df['Width'])**2

SIZES = list(range(6, 22, 3))
COLORS = Viridis9
N_SIZES = len(SIZES)
N_COLORS = len(COLORS)


columns = sorted(df.columns)
discrete = [x for x in columns if df[x].dtype == object]
continuous = [x for x in columns if x not in discrete]

def create_figure():
    xs = df[x.value].values
    ys = df[y.value].values
    x_title = x.value.title()
    y_title = y.value.title()

    kw = dict()
    if x.value in discrete:
        kw['x_range'] = sorted(set(xs))
    if y.value in discrete:
        kw['y_range'] = sorted(set(ys))
    kw['title'] = "%s vs %s" % (x_title, y_title)

    if coerseplottitle:
        kw['title'] = coerseplottitle.value
    else:
        pass

    p = figure(plot_height=1200, plot_width=1200, tools='pan,box_zoom,hover,reset', **kw)
    p.xaxis.axis_label = x_title
    p.yaxis.axis_label = y_title

    if x.value in discrete:
        p.xaxis.major_label_orientation = pd.np.pi / 4

    sz = 9
    if size.value != 'None':
        if len(set(df[size.value])) > N_SIZES:
            groups = pd.qcut(df[size.value].values, N_SIZES, duplicates='drop')
        else:
            groups = pd.Categorical(df[size.value])
        sz = [SIZES[xx] for xx in groups.codes]

    c = "#31AADE"
    if color.value != 'None':
        if len(set(df[color.value])) > N_SIZES:
            groups = pd.qcut(df[color.value].values, N_COLORS, duplicates='drop')
        else:
            groups = pd.Categorical(df[color.value])
        c = [COLORS[xx] for xx in groups.codes]

    p.circle(x=xs, y=ys, color=c, size=sz, line_color="white", alpha=0.6, hover_color='white', hover_alpha=0.5)
    
    try:
        if (x_axis_min != 'None'):
            p.x_range.start = float(minx)
        else:
            pass


        if (x_axis_max != 'None'):
            p.x_range.end = float(maxx)
        else:
            pass

    except:
        pass

    try:
        if (y_axis_min != 'None'):
            p.y_range.start = float(miny)
        else:
            pass    

        if (y_axis_max != 'None'):
            p.y_range.end = float(maxy)
        else:
            pass

    except:
        pass


    if (x_err.value != 'None'):
        xerr = df[x_err.value].values
        x_err_x = []
        x_err_y = []
        for px, py, err in zip(xs, ys, xerr):
            x_err_x.append((px - err, px + err))
            x_err_y.append((py, py))
        p.multi_line(x_err_x, x_err_y, color=c)

    if (y_err.value != 'None'):
        yerr = df[y_err.value].values
        y_err_x = []
        y_err_y = []
        for px, py, err in zip(xs, ys, yerr):
            y_err_x.append((px, px))
            y_err_y.append((py - err, py + err))
        p.multi_line(y_err_x, y_err_y, color=c)


    ticksize = ticksfontsize.value
    axistitlesize = axistitlefontsize.value
    titlesize = titlefontsize.value

    if coersextitle:
        p.xaxis.axis_label = coersextitle.value
    else:
        pass

    if coerseytitle:
        p.yaxis.axis_label = coerseytitle.value
    else:
        pass
  

    p.axis.major_label_text_font_size = value(ticksize)
    p.axis.axis_label_text_font_size = value(axistitlesize)
    p.title.text_font_size = value(titlesize)

    return p


def update(attr, old, new):
    graphs.children[1] = create_figure()


x = Select(title='X-Axis', value=df.columns[0], options=columns)
x.on_change('value', update)

y = Select(title='Y-Axis', value=df.columns[0], options=columns)
y.on_change('value', update)

x_err = Select(title = 'X-Axis error', value = 'None', options = columns+ ['None'])
x_err.on_change('value', update)

y_err = Select(title = 'Y-Axis error', value = 'None', options = columns+ ['None'])
y_err.on_change('value', update)

size = Select(title='Size', value='None', options=['None'] + continuous)
size.on_change('value', update)

color = Select(title='Color', value='None', options=['None'] + continuous)
color.on_change('value', update)

ticksfontsize = TextInput(title= 'Axis Values font size', value = '20pt')
ticksfontsize.on_change('value',update)
axistitlefontsize = TextInput(title= 'Both Axis title Font size', value = '20pt')
axistitlefontsize.on_change('value',update)
titlefontsize = TextInput(title= 'Title font size', value = '20pt')
titlefontsize.on_change('value',update)

coersextitle = TextInput(title= 'Force the X-Axis title to', value = '')
coersextitle.on_change('value',update)
coerseytitle = TextInput(title= 'Force the Y-Axis title to', value = '')
coerseytitle.on_change('value',update)
coerseplottitle = TextInput(title= 'Force the plot title to', value = '')
coerseplottitle.on_change('value',update)

controls = widgetbox([x, y, x_err, y_err,color, size], width=250)
axiscontrols = widgetbox([ticksfontsize,axistitlefontsize,titlefontsize,coersextitle,coerseytitle,coerseplottitle],width =250)

title = row(desc)
graphs = row(controls,create_figure(),axiscontrols)
layout = column(title,graphs)

curdoc().add_root(layout)

curdoc().add_root(layout)
curdoc().title = "C(NALYZER)"