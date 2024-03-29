import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer

class KuropolyConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['idRoom']
        self.room_group_name = 'room_%s' % self.room_name
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        print("Disconnected")
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        """
        Receive message from WebSocket.
        Get the event and send the appropriate event
        """
        response = json.loads(text_data)
        event = response.get("event", None)
        message = response.get("message", None)
            
        if event == 'START':
            # Send message to room group
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'send_message',
                'message': message,
                'event': "START"
            })
            
        if event == 'END':
            # Send message to room group
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'send_message',
                'message': message,
                'event': "END"
            })

        if event == 'COBRAR':
            # Send message to room group
            transaction = response.get("transaction", None)
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'send_message',
                'message': message,
                'event': "COBRAR",
                'transaction': {
                        'from': transaction['user_from'],
                        'to': transaction['to'],
                        'amount': transaction['amount']
                    }
        })

        if event == 'PASS_GO':
            # Send message to room group
            transaction = response.get("transaction", None)
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'send_message',
                'message': message,
                'event': "PASS_GO",
                'transaction': {
                        'from': transaction['user_from'],
                        'to': transaction['to'],
                        'amount': transaction['amount']
                    }
        })

        if event == 'TRAN':
            #Send message to users 
            transaction = response.get("transaction", None)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                'type': 'send_message',
                'message': message,
                'event': "TRAN",
                'transaction': {
                        'from': transaction['user_from'],
                        'to': transaction['to'],
                        'amount': transaction['amount']
                    }
                }
            )

    async def send_message(self, res):
        """ Receive message from room group """
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "payload": res,
        }))

    # async def chat_message(self, event):
    #     """
    #     Called when someone has messaged our chat.
    #     """
    #     # Send a message down to the client
    #     await self.send_json(
    #         {
    #             "msg_type": settings.MSG_TYPE_MESSAGE,
    #             "room": event["idRoom"],
    #             "username": event["username"],
    #             "message": event["message"],
    #         },
    #     )