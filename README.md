# Facedescriber
(EE) Veebirakendus nägude kirjeldamiseks pilditöötluse abil
(EN) Web application for facial description via image processing

## Arhitektuur/Architecture
(EE) Facedescriber koosneb eraldatud Vue frontend ja Java backend teenustest, lisaks Node.js ümbersuunamisserver HTTP päringute jaoks. Algoritm on realiseeritud Pythoni abil.
(EN) Facedescriber consists of separated Vue frontend and Java backend services, as well as a Node.js redirect server for HTTP requests. Python is used for the algorithm itself.


## Backend
(EE) Backend teenuse käivitamiseks piisab FaceDescriberApplication.java jooksutamisest. Pythoni virtuaalkeskkonna loomise ja kõige muuga tegeleb see ise.
(EN) In order to run the backend service, it is enough to just run FaceDescriberApplication.java. It will create the necessary Python virtual environment and everything else it needs by itself.


## Frontend
(EE) Frontend teenuse käivitamiseks tuleb jooksutada skripti ("/usr/bin/env bash src/frontend/startFrontendService.sh"). Vaja on sudo õiguseid.
(EN) In order to run the frontend service, run the script ("/usr/bin/env bash src/frontend/startFrontendService.sh"). Sudo permissions are needed.

# Märkmed/Notes
(EE) See repositoorium sisaldab iseallkirjastatud serti https toe jaoks. Brauserid seda serti vaikimisi ei usalda.
(EN) This repository contains a self-signed certificate for https support. Browsers will not trust the certificate by default.



