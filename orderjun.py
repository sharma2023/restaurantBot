from linebot.models import (
    ButtonsTemplate, MessageAction, TemplateSendMessage
)

order_template_message = TemplateSendMessage(
        alt_text='表示の順を設定',
        template=ButtonsTemplate(
            title='表示の順を設定',
            text='表示の順を設定してください',
            actions=[
                MessageAction(
                    label='店名かな順',
                    text='店名かな順'
                ),
                MessageAction(
                    label='ジャンルコード順',
                    text='ジャンルコード順'
                ),
                MessageAction(
                    label='小エリアコード順',
                    text='小エリアコード順'
                ),
                MessageAction(
                    label='おススメ順',
                    text='おススメ順'
                )
            ]
        )
    )