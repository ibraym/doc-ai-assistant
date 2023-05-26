import panel as pn

from qa.qa import HuggingFaceQA

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

canvas = []  # store all panel objects in a list
def qa_result(_):
    # save pdf file to a temp file
    if file_input.value is not None:
        file_input.save("data/datasets/temp.pdf")
    prompt_text = prompt.value
    if prompt_text:
        qa_model = HuggingFaceQA("data/datasets")
        result = qa_model.answer(prompt_text)
        canvas.extend([
            pn.Row(
                pn.panel("\U0001F60A", width=10),
                prompt_text,
                width=600
            ),
            pn.Row(
                pn.panel("\U0001F916", width=10),
                pn.Column(
                    result,
                    "Relevant source text:",
                    pn.pane.Markdown(result)
                )
            )
        ])
        #return canvas
    return pn.Column(*canvas, margin=15, width=575, min_height=400)

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

