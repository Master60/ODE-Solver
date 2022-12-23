import PySimpleGUI as sg
from utilsODE import *
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

sg.theme('LightGrey1')
FONT = 'Hilvetica 15'
DASHES = ['dy/dx','d2y/dx2','d3y/dx3']
METHODS = ["Euler's Method", "Heun's Method", "Midpoint Method", "Ralston's Method", "RK3", "RK4", "Butcher's RK5"]
expression = ''
initialcond = ''
h = 0
xout_step=0
xf = 0
x=0
y=np.array([0])


def block_focus(window):
    for key in window.key_dict:    # Remove dash box of all Buttons
        element = window[key]
        if isinstance(element, sg.Button):
            element.block_focus()

def popup_initial(order):

    col_layout = [[sg.Button('OK',key='-CLI-',bind_return_key=True)]]
    layout = [
        [sg.Text("Enter Initial Conditions\n")],
        [sg.Text("x = ",font=FONT),sg.Input(key='-xinit-')],
        [sg.Text("y = ",font=FONT),sg.Input(key='-yinit-')]

    ]

    for i in range(1, order):
            layout.append([sg.Text("y" + "'" * i + "= ", font=FONT), sg.Input(key = "-y" + "d"*i + "init-")])
    layout.append([sg.Column(col_layout,expand_x=True, element_justification='right')])
    window = sg.Window("Initial Conditions", layout, use_default_focus=False,return_keyboard_events=True, finalize=True, modal=True,size=(300,300))
    block_focus(window)
    while True:
        event, values = window.read()
        if event in [sg.WIN_CLOSED,'-CLI-']:
            break
    window.close()
    return values

def update_figure(x,y,format,label):
    axes = fig.axes
    axes[0].plot(x,y,format,label=label)
    axes[0].legend()
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack()

def eval_ts(expression,x0,xf):
    if(expression==None or expression==''):return [],[]
    xs = np.linspace(x0,xf,max(int((xf-x0)/h),50,int((xf-x0)/0.1)))
    ys=[]
    for x in xs:
        ys.append(eval(expression))
    return xs,ys

menu_layout = [
    ['File',['Save','Open','---','Exit']],
    ['About'],
    ['Help']
]

layout = [
    [sg.Menu(menu_layout)],
    [sg.Push(),sg.Text('ODE Solver',font='Hilvetica 30'),sg.Push()],
    [sg.Text('Order',font=FONT),sg.Spin([1,2,3,4,5],size=(5,1),font=FONT,readonly=True,enable_events=True,key='-ORDER-'),sg.Push(),
    sg.Text('',visible=False,key='-init-',font=FONT)],
    [sg.Text("y'=",key='-YDASH-',font=FONT),sg.Input(size=(27,4),font=FONT,key='-EQU-',enable_events=True,tooltip='dy/dx type in yp1 \nd2y/dx2 type in yp2 and so on..'),
    sg.Push(),sg.Button('Initial Conditions',key='-BTN_INIT-',font=FONT)],
    [sg.Text('Step Size (h)=',font=FONT),sg.Input(size=(10,4),font=FONT,key='-STP-',enable_events=True),sg.Push(),sg.Text("Method: ", font=FONT), sg.Combo(key='-METHOD-', values=METHODS, default_value="RK4", enable_events=True, readonly=True)],
    [sg.Text('Out Interval = ',font=FONT),sg.Input(size=(10,4),font=FONT,key='-STPOUT-',enable_events=True), sg.Push(),
    sg.Text("Final x = ",font=FONT),sg.Input(key='-xfinit-',size=(10,4),font=FONT)],
    [sg.Text('Solution:  y  = ',font=FONT),sg.Input(size=(40,4),font=FONT,key='-GEQU-',enable_events=True,tooltip='dy/dx type in yp1 \nd2y/dx2 type in yp2 and so on..')],
    [sg.Button('Solve',font=FONT,key='-SOLVE-'),sg.Button('Reset',font=FONT,key='-RESET-',button_color=('#FFFFFF', '#FF0000'))],
    [sg.Canvas(key='-CANVAS-')]
]

window = sg.Window(title='ODE Solver',layout=layout,size=(580,700),finalize=True)

def create_plot():
    global fig,figure_canvas_agg
    fig = matplotlib.figure.Figure(figsize=(5,4))
    fig.add_subplot(111).plot([],[])
    figure_canvas_agg = FigureCanvasTkAgg(fig,window['-CANVAS-'].TKCanvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack()

def reset_plot():
    canvas = window['-CANVAS-'].TKCanvas
    canvas.delete("all")
    figure_canvas_agg.get_tk_widget().forget()
    plt.close('all')
    create_plot()

def reset_vals():
    global expression,initialcond,h,xout_step,xf,x,y
    expression = ''
    initialcond = ''
    h = 0
    xout_step=0
    xf = 0
    x=0
    y=np.array([0])
    window['-EQU-'].update('')
    window['-init-'].update('',visible=False)
    window['-STP-'].update('')
    window['-STPOUT-'].update('')
    window['-GEQU-'].update('')
    window['-xfinit-'].update('')
    window['-CANVAS-'].update()
    window['-METHOD-'].update('RK4')
    reset_plot()


create_plot()

while True:
    event,values = window.read()
    if event == sg.WIN_CLOSED:
        break

    if event == '-ORDER-':
        order = int(values['-ORDER-'])
        ystr = 'y' + "'" * order +'= '

        window['-YDASH-'].update(ystr)
        initialcond=None
        window['-init-'].update('',visible=False)

    if event == '-EQU-':
        expression = values['-EQU-']


    if event == '-BTN_INIT-':
        order = values['-ORDER-']
        icd = popup_initial(order)
        if(icd==None):continue
        initialcond=icd
        initstr = 'Initial Point:'+ ' (' + initialcond['-xinit-'] +', '+ initialcond['-yinit-']
        for i in range(1, order):
            initstr += ', ' + initialcond['-y' + 'd' * i + 'init-']
        initstr+=')'

        window['-init-'].update(initstr,visible=True)
    if event == '-SOLVE-':
        try:
            reset_plot()
            method_idx = METHODS.index(values['-METHOD-'])
            xf = float(values['-xfinit-'])
            h = float(values['-STP-'])
            xout_step = float(values['-STPOUT-'])
            x=float(initialcond['-xinit-'])
            n = values['-ORDER-']
            y=np.array([0]*n)
            y[0] = float(initialcond['-yinit-'])
            for i in range(1, n):
                y[i] = float(initialcond['-y' + 'd' * i + 'init-'])
            x_true,y_true = eval_ts(values['-GEQU-'],x,xf)
            xout,yout = solveODE(x, y, xf, h, xout_step, expression, method_idx)
            update_figure(xout,yout,'r-','ODE Approx.')
            update_figure(x_true,y_true,'b-','True Solution')
        except:
            sg.popup_error()
    if event =='-RESET-':
        reset_vals()
        print(xf,h,y,xout_step,expression)
        print('rest')

window.close()