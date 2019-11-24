import time
import multiprocessing as mp
from .soccerpy.agent import Agent as baseAgent
from .soccerpy.world_model import WorldModel
from .soccerpy.game_object import Flag

# TODO:decision内の実装(最低限の行動モジュールを作成)

TEAM_NAME = "ALPHA"
PLAYER_NUM = 11

turn_count = 0

class MyAgent(baseAgent):
    """
    baseAgentからの継承クラスを作成。
    意思決定部分と行動の関数のみ用意するようにする。
    """
    def think(self):
        """
        親クラスbaseAgentで__think_threadを作り__think_loop内でthink()が呼ばれループ処理される。

        wm.is_before_kick_off():キックオフ前ならTrue、キックオフ後ならFalse
        wm.is_kick_off_us():自チームのキックオフならTrue、敵チームのキックオフならFalse
        wm.is_playon():ゲームをプレイできない状態（キックオフ、コーナーキック、フリーキック)はTrue、プレイできる状態はFalse
        in_kick_off_formuration:baseAgent.play()でsetup_environment()が呼ばれそこでin_kick_off_formurationはFalseになる
        :return: なし
        """

        # ここでキックオフ前のポジションを設定する
        if not self.in_kick_off_formation:

            # チームがどちらのサイドで始めるかで初期ポジションを反転させる。
            side_mod = 1
            if self.wm.side == WorldModel.SIDE_R:
                side_mod = -1

            # 指定の座標に移動させる
            if self.wm.uniform_number == 1:
                self.wm.teleport_to_point((-5 * side_mod, 30))
            elif self.wm.uniform_number == 2:
                self.wm.teleport_to_point((-40 * side_mod, 15))
            elif self.wm.uniform_number == 3:
                self.wm.teleport_to_point((-40 * side_mod, 00))
            elif self.wm.uniform_number == 4:
                self.wm.teleport_to_point((-40 * side_mod, -15))
            elif self.wm.uniform_number == 5:
                self.wm.teleport_to_point((-5 * side_mod, -30))
            elif self.wm.uniform_number == 6:
                self.wm.teleport_to_point((-20 * side_mod, 20))
            elif self.wm.uniform_number == 7:
                self.wm.teleport_to_point((-20 * side_mod, 0))
            elif self.wm.uniform_number == 8:
                self.wm.teleport_to_point((-20 * side_mod, -20))
            elif self.wm.uniform_number == 9:
                self.wm.teleport_to_point((-10 * side_mod, 0))
            elif self.wm.uniform_number == 10:
                self.wm.teleport_to_point((-10 * side_mod, 20))
            elif self.wm.uniform_number == 11:
                self.wm.teleport_to_point((-10 * side_mod, -20))

            # ポジションセット完了後のフラグセット
            self.in_kick_off_formation = True

            return

        # 自陣ゴールと敵陣ゴールの座標をセット
        # TODO: なぜゴール座標をセットするのか
        if self.wm.side == WorldModel.SIDE_R:
            self.enemy_goal_pos = (-55, 0)
            self.own_goal_pos = (55, 0)
        else:
            self.enemy_goal_pos = (55, 0)
            self.own_goal_pos = (-55, 0)

        # 意思決定できる状態にdecision関数を呼び出す。
        if not self.wm.is_before_kick_off() or self.wm.is_kick_off_us() or self.wm.is_playon():
            self.decision()
        return

    # 意思決定部分
    def decision(self):
            # 1番のみ行動を行う
        if self.wm.uniform_number == 1:
            if self.wm.ball is not None:
                pos = self.wm.my_obj_pos(self.wm.ball)
                vec = self.wm.my_obj_vel(self.wm.ball)
                print(vec)
            else:
                self.wm.ah.turn(5.0)

    def find_ball(self):
        if self.wm.ball is None or self.wm.ball.direction is None:
            self.wm.ah.turn(30)
        else:
            return True
        return False

    def move_to_ball(self):
        if self.find_ball():
            self.wm.turn_body_to_object(self.wm.ball)
            self.wm.ah.dash(30)

    def kick_to_goal(self):
        if self.wm.is_ball_kickable():
            self.wm.kick_to(self.enemy_goal_pos, 1.0)
        else:
            self.move_to_ball()




if __name__ == "__main__":

    def spawn_agent(team_name, position):
        a = MyAgent()
        a.connect("localhost", 6000, team_name)
        a.play()
        print("spawning agent {0}".format(position))
        if not position  == 1:
            while True:
                time.sleep(1)

    spawn_agent(TEAM_NAME, 1)

    # ユニフォーム番号が2番以降はほかプロセスで作成する
   # for position in range(2, PLAYER_NUM+1):
   #     at = mp.Process(target=spawn_agent, args=(TEAM_NAME, position))
   #     at.daemon = True
   #     at.start()

    while True:
        time.sleep(1)
