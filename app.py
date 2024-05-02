from flask import Flask, request

app = Flask(__name__)

@app.route('/hasura-trigger', methods=['POST'])
def hasura_trigger():
    # Handle the Hasura event trigger here
    # Extract data from the request and perform necessary actions
    data = request.json
    print("Event Trigger Data:", data)

    # Perform necessary actions based on the event data

    return 'Event received successfully'

if __name__ == '__main__':
    # Start ngrok
    from pyngrok import ngrok
    ngrok_tunnel = ngrok.connect(5000)
    print('Public URL:', ngrok_tunnel.public_url)

    # Run the Flask app
    app.run()
