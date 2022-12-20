import PySimpleGUI as sg
from utilsODE import *
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

sg.theme('LightGrey1')
FONT = 'Hilvetica 15'
DASHES = ['dy/dx','d2y/dx2','d3y/dx3']
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
    if order>=2 :
        layout.append([sg.Text("y' = ",font=FONT),sg.Input(key='-ydinit-')])
    if order>=3:
        layout.append([sg.Text("y'' = ",font=FONT),sg.Input(key='-yddinit-')])
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
    #print('----- in update fig -----')
    axes = fig.axes
    axes[0].plot(x,y,format,label=label)
    axes[0].legend()
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack()

def eval_gs(expression,x0,xf):
    #print('----eval gs----')
    if(expression==None or expression==''):return [],[]
    #print('calc gs')
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
    [sg.Text('Order',font=FONT),sg.Spin([1,2,3],size=(5,1),font=FONT,readonly=True,enable_events=True,key='-ORDER-'),sg.Push(),
    sg.Text('',visible=False,key='-init-',font=FONT)],
    [sg.Text("y'=",key='-YDASH-',font=FONT),sg.Input(size=(30,4),font=FONT,key='-EQU-',enable_events=True,tooltip='dy/dx type in yp1 \nd2y/dx2 type in yp2 and so on..'),
    sg.Push(),sg.Button('Initial Conditions',key='-BTN_INIT-',font=FONT)],
    [sg.Text('Enter step size h=',font=FONT),sg.Input(size=(10,4),font=FONT,key='-STP-',enable_events=True),sg.Text("x final = ",font=FONT),sg.Input(key='-xfinit-',size=(10,4),font=FONT)],
    [sg.Text('GS (optional) y=',font=FONT),sg.Input(size=(30,4),font=FONT,key='-GEQU-',enable_events=True,tooltip='dy/dx type in yp1 \nd2y/dx2 type in yp2 and so on..')],
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
    window['-GEQU-'].update('')
    window['-xfinit-'].update('')
    window['-CANVAS-'].update()
    reset_plot()
    
    
create_plot()

while True:
    event,values = window.read()

    if event == sg.WIN_CLOSED:
        break

    if event == '-ORDER-':
        ystr = 'y' + "'"*int(values['-ORDER-']) +'= '
        window['-YDASH-'].update(ystr)
        initialcond=None
        window['-init-'].update('',visible=False)

    if event == '-EQU-':
        expression = values['-EQU-']
        

    if event == '-BTN_INIT-':
        icd = popup_initial(values['-ORDER-'])
        if(icd==None):continue
        initialcond=icd
        initstr = 'Initial Point:'+ ' (' + initialcond['-xinit-'] +', '+ initialcond['-yinit-']
        if '-ydinit-' in initialcond.keys():initstr+= ', ' + initialcond['-ydinit-']
        if '-yddinit-' in initialcond.keys():initstr+=', '  + initialcond['-yddinit-']
        initstr+=')'
        
        window['-init-'].update(initstr,visible=True)
        #print(initialcond)
    if event == '-SOLVE-':
        try:
            reset_plot()
            xf = float(values['-xfinit-'])
            h = float(values['-STP-'])
            x=float(initialcond['-xinit-'])
            n = values['-ORDER-']
            y=np.array([0]*n)
            y[0] = float(initialcond['-yinit-'])
            if(n>=2):y[1]=float(initialcond['-ydinit-'])
            if (n>=3):y[2]=float(initialcond['-yddinit-'])
            #print(xf,h,n,x,y,expression,values['-GEQU-'])
            xout_step=h+0.1
            xgs,ygs = eval_gs(values['-GEQU-'],x,xf)
            xout,yout = solveODE(x, y, xf, h, xout_step, expression)
            #print('CAlculated ode')
            update_figure(xout,yout,'r-','ODE Approx.')
            #print('drawn ode')
            #print(xgs,ygs)
            update_figure(xgs,ygs,'b-','General Solution')
        except:
            sg.popup_error()
    if event =='-RESET-':
        reset_vals()
        print(xf,h,y,xout_step,expression)
        print('rest')
    
window.close()