# Facedescriber
(EE) Veebirakendus nägude kirjeldamiseks pilditöötluse abil.\
(EN) Web application for facial description via image processing.

## Arhitektuur/Architecture
(EE) Facedescriber koosneb eraldatud Vue frontend ja Java backend teenustest, lisaks Node.js ümbersuunamisserver HTTP päringute jaoks. Näokirjeldus on realiseeritud Pythoni abil. Lihtsustatud ülevaade: simple_architecture.png\
(EN) Facedescriber consists of separated Vue frontend and Java backend services, as well as a Node.js redirect server for HTTP requests. Python is used for the facial description itself. Simplified overview: simple_architecture.png

## Backend
(EE) Backend teenuse püsti seadmiseks tuleb luua Pythoni virtuaalkeskkond ja installeerida vajalikud moodulid. Selleks on olemas skript, mida tuleb jooksutada vaid üks kord ("sudo /usr/bin/env bash src/main/python/setup.sh). Edaspidi piisab teenuse käivitamiseks FaceDescriberApplication.java jooksutamisest.\
(EN) In order to set up the backend service, you need to create a Python virtual environment and install the necessary dependencies. There is a one-time script for this ("sudo /usr/bin/env bash src/main/python/setup.sh). After that, in order to run the backend service, it is enough to just run FaceDescriberApplication.java.

### Backend API
(EE) Suhtlus frontend ja backend teenuste vahel on realiseeritud REST programmeerimisliidesega backend teenuses, millele pääsevad ligi ka teised kliendid. Näiteid erinevatest Bash päringutest saab leida siit: src/main/java/examples/examples.md.\
(EN) Communication between the frontend and backend services is realized using a REST API in the backend service, which can also be accessed by other clients. Examples of different calls to the API using Bash commands are found in src/main/java/examples/examples.md.

## Frontend
(EE) Frontend teenuse käivitamiseks tuleb jooksutada skripti ("/usr/bin/env bash src/frontend/startFrontendService.sh"). Vaja on sudo õiguseid.\
(EN) In order to run the frontend service, run the script ("/usr/bin/env bash src/frontend/startFrontendService.sh"). Sudo permissions are needed.

## Tarkvara/Software
Ubuntu 22.04.2 LTS \
Java 17 \
Maven 3.9.5 \
Spring Boot 3.1.4 \
Python 3.10 \
Vue 3.37.0 \
vue/cli 5.0.8 \
Node.js v18.18.0 \
npm 9.8.1

## Märkmed/Notes
(EE) See repositoorium sisaldab iseallkirjastatud serti https toe jaoks. Brauserid seda serti vaikimisi ei usalda.\
(EN) This repository contains a self-signed certificate for https support. Browsers will not trust the certificate by default.

(EE) Ekstra materjalid (esindajate leidmine, kirjeldajate näidisväljundid) on saadaval kaustas src/main/python/extras.\
(EN) Extra material (finding the representatives, examples of the describers' output) is available in src/main/python/extras.


