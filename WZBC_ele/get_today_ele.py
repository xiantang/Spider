import requests
import pymysql
import  time
def run():
    connect = pymysql.Connect(
        host='',
        port=3306,
        user='root',
        passwd='123456',
        db='electric',
        charset="utf8"

    )
    sql = """SELECT * 
    from room"""
    cursors = connect.cursor()
    cursors.execute(sql)
    room_list = []
    for i in cursors.fetchall():
        room_list.append(i)

    for i in room_list:
        bulid_Id = i[3]

        room_id = i[1]
        try:
            c = requests.get(
                "http://pay.wzbc.edu.cn/api/pay/wzbc/query/bill?zoneId=1&buildId={bulid_Id}&roomId={room_id}".format(
                    bulid_Id=bulid_Id, room_id=room_id)).json()
            created = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            allAmp = c[0]["allAmp"]
            usedAmp = c[0]["usedAmp"]
            currentAmp = allAmp - usedAmp
            roomName = c[0]['room']
            sql = """
            INSERT INTO `electric` (`roomId`, `roomName`, `usedAmp`, `allAmp`, \
            `currentAmp`, `created`) VALUES ('{roomId}', '{roomName}', '{usedAmp}'\
            , '{allAmp}', '{currentAmp}', '{created}')  ON DUPLICATE KEY UPDATE \
            usedAmp='{usedAmp}',allAmp='{allAmp}',currentAmp='{currentAmp}'"""
            sql = sql.format(roomId=room_id,roomName=roomName,usedAmp=usedAmp,
                       allAmp=allAmp,currentAmp=currentAmp,created=created)
            cursors.execute(sql)
            #time.strftime('%Y.%m.%d', time.localtime(time.time()))
        except:
            print("e")
    connect.commit()
if __name__ == '__main__':
    run()