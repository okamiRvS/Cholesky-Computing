# **Assignment 1 : Cholesky Computing**
* Alberici Federico - 808058
* Bettini Ivo Junior - 806878
* Cocca Umberto - 807191
* Traversa Silvia - 816435

# Introduzione
Lo scopo di questo progetto è studiare l’implementazione del metodo di Cholesky per la risoluzione di sistemi lineari con matrici sparse, simmetriche e definite positive, in ambienti di programmazione open source e confrontarla con l’implementazione MATLAB. Questo confronto viene eseguito su due sistemi operativi diversi, Windows e Linux. Per ognuna delle matrici calcoliamo:
* Il tempo necessario per calcolare la soluzione x del sistema lineare Ax=b 
* L’errore relativo tra la soluzione calcolata x e la soluzione esatta xe, trovata come soluzione del sistema Axe=B
* La memoria necessaria per risolvere il sistema, ovvero l’aumento della dimensione del programma in memoria da subito dopo aver letto la matrice a dopo aver risolto il sistema.

Per poter raggiungere questo obiettivo abbiamo deciso di confrontare MATLAB con gli ambienti open source C++, R e Python.

# Analisi dei risultati
Le matrici simmetriche e definite positive che abbiamo considerato per la relazione fanno parte della **SuiteSparse Matrix Collection** che colleziona matrici sparse derivanti da
applicazioni di problemi reali (ingegneria strutturale, fluidodinamica, elettromagnetismo, termodinamica, computer graphics/vision, network e grafi).

In particolare le matrici simmetriche e definite positive che abbiamo analizzato sono le seguenti:
- [Flan 1565](https://sparse.tamu.edu/Janna/Flan_1565)
- [StocF-1465](https://sparse.tamu.edu/Janna/StocF-1465)
- [cfd2](https://sparse.tamu.edu/Rothberg/cfd2)
- [cfd1](https://sparse.tamu.edu/Rothberg/cfd1)
- [G3 circuit](https://sparse.tamu.edu/AMD/G3_circuit)
- [parabolic fem](https://sparse.tamu.edu/Wissgott/parabolic_fem)
- [apache2](https://sparse.tamu.edu/GHS_psdef/apache2)
- [shallow water1](https://sparse.tamu.edu/MaxPlanck/shallow_water1)
- [ex15](https://sparse.tamu.edu/FIDAP/ex15)

Per poterle testarle basta scaricare le matrici .mtx dei link precedenti e inserirle nella cartella [data](https://gitlab.com/okamiRvS/cholesky-computing/-/tree/master/data) e poi avviare i vari programmi, da linea di comando, contenuti nella cartella src e da applicazione per quanto riguarda Matlab. 

Per l’analisi confrontiamo i grafici derivanti dai risultati ottenuti in output dalle varie esecuzioni dei linguaggi nei due sistemi operativi Linux e Windows. È importante notare che la Flan 1565 e la StocF-1465 viste le loro notevoli dimensioni, non sono state possibile eseguirle sui nostri computer. La raccolta dei dati è avvenuta su un unico pc provvisto di macchina virtuale per entrambi i sistemi operativi, in modo tale da avere una potenza di calcolo confrontabile statisticamente. Le specifiche tecniche sono le seguenti:

Windows x64\
*Processor: Intel(R) Core(TM) i5-4460 CPU @ 3.20GHz, Number of cores: 4, Memory: Ram 11000 MB.*

Unix x64\
*Kernel: 5.3.0-53-generic, Processor: Intel(R) Core(TM) i5-4460 CPU @ 3.20GHz, Number of cores: 4, Memory: Ram 11000 MB.*

# Conclusioni
Nel sistema operativo Windows nessuno dei linguaggi analizzati dimostra di riuscire ad eseguire i calcoli in un tempo totale (calcolato come somma del tempo necessario per
l’importazione della matrice e del tempo necessario per la decomposizione di Cholesky) particolarmente migliore rispetto agli altri.

<div align="center">
<img src="https://gitlab.com/okamiRvS/cholesky-computing/-/raw/master/final%20results/img/tempoimpwin.png" >
<p>Fig. 1: Tempo esecuzione totale su Windows</p>
</div>

<br />

Per quanto riguarda Linux C++ e R risultano avere andamenti simili a Windows. Python, invece, mostra un’esecuzione molto più rapida rispetto a Windows rendendolo il migliore a tutti gli altri linguaggi utilizzati.
<div align="center">
<img src="https://gitlab.com/okamiRvS/cholesky-computing/-/raw/master/final%20results/img/tempototlinux.png" >
<p>Fig. 2: Tempo esecuzione totale su Linux</p>
</div>

Si rimanda alla [relazione](https://gitlab.com/okamiRvS/cholesky-computing/-/blob/master/final%20results/Relazione.pdf) per un'analisi completa e dettagliata.
