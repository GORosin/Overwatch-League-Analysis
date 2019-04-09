from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
import sys
from owl_elo import inter_stage_ranking as rank_teams
Ui_MainWindow, QtBaseClass = uic.loadUiType("OWLGui.ui")


class MyApp(QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.csv="stage2.csv"
        self.ui.Team1Round1.setText('0')
        self.ui.Team1Round2.setText('0')
        self.ui.Team1Round3.setText('0')
        self.ui.Team1Round4.setText('0')
        self.ui.Team1Round5.setText('0')
        self.ui.Team2Round1.setText('0')
        self.ui.Team2Round2.setText('0')
        self.ui.Team2Round3.setText('0')
        self.ui.Team2Round4.setText('0')
        self.ui.Team2Round5.setText('0')
        self.ui.AddMatch.clicked.connect(self.update_scores)
        self.ui.iterations.setText("10")
        self.ui.update.setText("30")
        self.ui.calculate.clicked.connect(self.DisplayRanking)

    def DisplayRanking(self):
        try:
            iterations=int(self.ui.iterations.toPlainText())
        except:
            print("using default iterations")
            iterations=10
        try:
            update=int(self.ui.update.toPlainText())
        except:
            print("using default update")
            update=30
        try:
            elo_reduction=float(self.ui.reduction.toPlainText())
            if elo_reduction > 1 or elo_reduction <0:
                raise ValueError
        except:
            elo_reduction=0
            print("using default elo reduction")
        rankings=rank_teams(iterations,update)
        ranks=""
        for i in rankings[::-1]:
            ranks+="team:"+str(i[0])+" elo:"+str(int(i[1]))+"\n"
            
        self.ui.DisplayRank.setText(ranks)
    def update_scores(self):
        team1=self.ui.Team1.toPlainText().upper()
        team2=self.ui.Team2.toPlainText().upper()
        team1_score=0
        team2_score=0
        with open(self.csv,'a') as scores:
            scores.write("\n")
            scores.write(team1)
            scores.write(",")
            scores.write(team2)
            scores.write(",")
            scores.write(self.ui.Team1Round1.toPlainText())
            scores.write(",")
            scores.write(self.ui.Team2Round1.toPlainText())
            scores.write(",")
            team1_score+=int(int(self.ui.Team1Round1.toPlainText())>int(self.ui.Team2Round1.toPlainText()))
            team2_score+=int(int(self.ui.Team1Round1.toPlainText())<int(self.ui.Team2Round1.toPlainText()))
            scores.write(self.ui.Team1Round2.toPlainText())
            scores.write(",")
            scores.write(self.ui.Team2Round2.toPlainText())
            scores.write(",")
            team1_score+=int(int(self.ui.Team1Round2.toPlainText())>int(self.ui.Team2Round2.toPlainText()))
            team2_score+=int(int(self.ui.Team1Round2.toPlainText())<int(self.ui.Team2Round2.toPlainText()))

            scores.write(self.ui.Team1Round3.toPlainText())
            scores.write(",")
            scores.write(self.ui.Team2Round3.toPlainText())
            scores.write(",")
            team1_score+=int(int(self.ui.Team1Round3.toPlainText())>int(self.ui.Team2Round3.toPlainText()))
            team2_score+=int(int(self.ui.Team1Round3.toPlainText())<int(self.ui.Team2Round3.toPlainText()))

            scores.write(self.ui.Team1Round4.toPlainText())
            scores.write(",")
            team1_score+=int(int(self.ui.Team1Round4.toPlainText())>int(self.ui.Team2Round4.toPlainText()))
            team2_score+=int(int(self.ui.Team1Round4.toPlainText())<int(self.ui.Team2Round4.toPlainText()))

            scores.write(self.ui.Team2Round4.toPlainText())
            scores.write(",")
            scores.write(self.ui.Team1Round5.toPlainText())
            scores.write(",")
            scores.write(self.ui.Team2Round5.toPlainText())
            team1_score+=int(int(self.ui.Team1Round5.toPlainText())>int(self.ui.Team2Round5.toPlainText()))
            team2_score+=int(int(self.ui.Team1Round5.toPlainText())<int(self.ui.Team2Round5.toPlainText()))

            scores.write(",")
            scores.write(str(team1_score))
            scores.write(",")
            scores.write(str(team2_score))
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
