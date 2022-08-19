from linebot.models import (
    ButtonsTemplate, MessageAction, TemplateSendMessage
)

buttons_template_message = TemplateSendMessage(
        alt_text='範囲設定',
        template=ButtonsTemplate(
            title='範囲設定',
            text='範囲を設定してください',
            actions=[
                MessageAction(
                    label='3キロ以内',
                    text='3キロ以内'
                ),
                MessageAction(
                    label='2キロ以内',
                    text='2キロ以内'
                ),
                MessageAction(
                    label='1キロ以内',
                    text='1キロ以内'
                ),
                MessageAction(
                    label='500メートル以内',
                    text='500メートル以内'
                )
            ]
        )
    )