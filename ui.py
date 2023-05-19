import panel as pn

pn.extension('texteditor', template='material', sizing_mode='stretch_width')
pn.state.template.param.update(
    title='AI Doc Assistant',
)

file_input = pn.widgets.FileInput(width=300)
prompt = pn.widgets.TextEditor(
    value='', placeholder='Enter your questions here...', height=160, toolbar=False
)
run_button = pn.widgets.Button(name='Run!')
widgets = pn.Row(pn.Column(prompt, run_button, margin=5),width=1000)

def qa_result(_):
    pass

qa_interactive = pn.panel(
    pn.bind(qa_result, run_button),
    loading_indicator=True,
)

output = pn.WidgetBox('*Output will show up here:*', qa_interactive, width=990, scroll=True)

pn.Column(
    pn.pane.Markdown('''
        Question Answering with your file\n
        Upload a file, type a question and click 'Run'.
    '''),
    pn.Row(file_input),
    widgets,
    output
).servable(target='main')

