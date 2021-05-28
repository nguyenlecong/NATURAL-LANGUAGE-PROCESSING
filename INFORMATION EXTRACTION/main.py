import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import NLP
import url_input
app = dash.Dash(__name__)
def connect(X):
    m=''
    for i in X:
        m+=str(i)+', '
    return m[:-2]
app.layout = html.Div([
    html.Div(children=[
        html.Div(children=[
            dcc.Input(
                id='url',
                style={'width': '44%'},
            ),
            html.Button(id='submit-button-state', n_clicks=0, children='Search'),
        ],style={'display':'block','vertical-align': 'top', 'margin-left': '5%', 'margin-top': '3vw'}),
        html.Div(children=[
            dcc.Textarea(
                id='textarea-example',
                value='Textarea content initialized\nwith multiple lines of text\n',
                style={'width': '50%', 'height': 300},
            ),
            
        ],style={'display':'block','vertical-align': 'top', 'margin-left': '5%','margin-right': '5%', 'margin-top': '3vw'}),
        html.Button('Submit', id='textarea-state-example-button', n_clicks=0, style={'margin-left': '5%'}),
        html.Div(id='textarea-example-output', style={'whiteSpace': 'pre-line','margin-left': '5%','margin-top': '3vw'})
    ])    
])
@app.callback(
    Output('textarea-example-output', 'children'),
    Input('textarea-state-example-button', 'n_clicks'),
    Input('submit-button-state', 'n_clicks'),
    State('textarea-example', 'value'),
    State('url', 'value')
)
def update_output(n_clicks, n_clicks1, value, value1):
    typeE, cateE, ae, road, dt, ct, pr, number, fullname = NLP.findAll(value)
    if value1 != '':
        soup = url_input.get_url(value1) 
        typeE, cateE, ae, road, dt, ct, pr, number, fullname = NLP.findAll(url_input.get_information(soup))
    m=''
    m+='Loại tin: '+connect(typeE)+'\n'
    m+='Loại nhà: '+connect(cateE)+'\n'
    m+='Diện tích: '+connect(ae)+'\n'
    m+='Đường: '+connect(road)+'\n'
    m+='Quận/huyện: '+connect(dt)+'\n'
    m+='Thành phố: '+connect(ct)+'\n'
    m+='Gía tiền: '+connect(pr)+'\n'
    m+='Số điện thoại: '+connect(number)+'\n'
    m+='Tên người liên hệ: '+connect(fullname)+'\n'
    return 'Result: \n{}'.format(m)

if __name__ == '__main__':
    app.run_server(debug=True)