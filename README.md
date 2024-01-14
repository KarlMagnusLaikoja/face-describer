# Facedescriber
(EE) Veebirakendus nägude kirjeldamiseks pilditöötluse abil.\
(EN) Web application for facial description via image processing.

## Arhitektuur/Architecture
(EE) Facedescriber koosneb eraldatud Vue frontend ja Java backend teenustest, lisaks Node.js ümbersuunamisserver HTTP päringute jaoks. Algoritm on realiseeritud Pythoni abil.\
(EN) Facedescriber consists of separated Vue frontend and Java backend services, as well as a Node.js redirect server for HTTP requests. Python is used for the algorithm itself.

## Backend
(EE) Backend teenuse käivitamiseks piisab FaceDescriberApplication.java jooksutamisest. Pythoni virtuaalkeskkonna loomise ja kõige muuga tegeleb see ise.\
(EN) In order to run the backend service, it is enough to just run FaceDescriberApplication.java. It will create the necessary Python virtual environment and everything else it needs by itself.

### Backend API
(EE) Suhtlus frontend ja backend teenuste vahel on realiseeritud REST programmeerimisliidesega, millele pääsevad ligi ka teised kliendid. Näiteid erinevatest päringutest Linuxi terminalis jooksutamiseks saab leida siit: src/main/java/examples/examples.md.\
(EN) Communication between the frontend and backend services is realized using a REST API, which can also be accessed by other clients. Examples of different calls to the API using Linux terminal are found in src/main/java/examples/examples.md.

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



