import teslajson
import vars
c = teslajson.Connection(vars.USERID, vars.PASS)
v = c.vehicles[0] # vehicles is an array. This assumes you only have one Tesla
v.wake_up()
data = v.data_request('drive_state')
print data
