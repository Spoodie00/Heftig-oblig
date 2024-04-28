import logging
import threading
import time
import requests

from messaging import ActuatorState
import common


class Actuator:

    def __init__(self, did):
        self.did = did
        self.state = ActuatorState('False')

    def simulator(self):

        logging.info(f"Actuator {self.did} starting")

        while True:

            logging.info(f"Actuator {self.did}: {self.state.state}")

            time.sleep(common.LIGHTBULB_SIMULATOR_SLEEP_TIME)

    def client(self):

        logging.info(f"Actuator Client {self.did} starting")

        # TODO: START
        # send request to cloud service with regular intervals and
        # set state of actuator according to the received response

        while True:
            try:
                # Hent tilstand fra sky-tjenesten
                response = requests.get(common.BASE_URL)
                if response.status_code == 200:
                    # Oppdater tilstanden til aktuatoren basert på responsen
                    self.state = ActuatorState.from_json(response.json())
                    logging.info(f"Actuator Client {self.did}: Fetched state: {self.state.state}")
                else:
                    logging.error(f"Actuator Client {self.did}: Failed to fetch state")
            except requests.RequestException as e:
                logging.error(f"Actuator Client {self.did}: Failed to connect to cloud service: {str(e)}")

            time.sleep(common.LIGHTBULB_CLIENT_SLEEP_TIME)


        logging.info(f"Client {self.did} finishing")

        # TODO: END

    def run(self):

        logging.info(f"Actuator{self.did} starting")
        # TODO: START

        # start thread simulating physical light bulb
        simulator_thread=threading.Thread(target=self.simulator)
        simulator_thread.start() 

        # start thread receiving state from the cloud
        client_thread=threading.Thread(target=self.client)
        client_thread.start()

        # TODO: END
actuator = Actuator(common.LIGHTBULB_DID)
actuator.run()