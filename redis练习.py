import redis


# 下载：https://github.com/tporadowski/redis/releases
# 解压：
# 运行：打开cmd窗口，使用cd命令切换redis文件夹目录，redis-server.exe redis.windows.conf / 打开redis文件夹，点击运行redis-server.exe
# 安装：pycharm，pip install redis
# 引入：import redis
# 使用：


# 连接池
# redis-py 使用 connection pool 来管理对一个 redis server 的所有连接，避免每次建立、释放连接的开销。
# 默认，每个Redis实例都会维护一个自己的连接池。可以直接建立一个连接池，然后作为参数 Redis，这样就可以实现多个 Redis 实例共享一个连接池。
pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
r = redis.Redis(connection_pool=pool)
r.set('zx', '001023', ex=5)
print(r.get('zx'))
r.delete('zx')
print(r.get('zx'))


print('\n' + '========== 一、redis基本命令：string ==========')
# set(name, value, ex=None, px=None, nx=False, xx=False)
# 在 Redis 中设置值，默认，不存在则创建，存在则修改。
# 参数：
# ex - 过期时间（秒）
# px - 过期时间（毫秒）
# nx - 如果设置为True，则只有name不存在时，当前set操作才执行
# xx - 如果设置为True，则只有name存在时，当前set操作才执行

# 1.ex - 过期时间（秒） 这里过期时间是3秒，3秒后p，键food的值就变成None
r.set('food', 'mutton', ex=3)  # key是'food' value是'mutton' 将键值对存入redis缓存
print('(1)', r.get('food'))  # mutton 取出键food对应的值

# 2.px - 过期时间（豪秒） 这里过期时间是3豪秒，3毫秒后，键foo的值就变成None
r.set('food', 'beef', px=3)
print('(2)', r.get('food'))

# 3.nx - 如果设置为True，则只有name不存在时，当前set操作才执行 （新建）
print('(3)', r.set('fruit', 'watermelon', nx=True))  # True--不存在
# 如果键fruit不存在，那么输出是True；如果键fruit已经存在，输出是None

# 4.xx - 如果设置为True，则只有name存在时，当前set操作才执行 （修改）
print('(4)', (r.set('fruit', 'watermelon', xx=True)))  # True--已经存在
# 如果键fruit已经存在，那么输出是True；如果键fruit不存在，输出是None

# 5.setnx(name, value)
# 设置值，只有name不存在时，执行设置操作（添加）
print('(5)', r.setnx('fruit1', 'banana'))  # fruit1不存在，输出为True；已存在则输出False

# 6.setex(name, time, value)
# time - 过期时间（数字秒 或 timedelta对象）
import time
r.setex('fruit2', 1, 'orange')
print('(6)', r.get('fruit2'))  # orange
time.sleep(1)  # 推迟1秒后再执行后面的程序
print('(6)', r.get('fruit2'))  # 1秒后，取值就从orange变成None

# 7.psetex(name, time_ms, value)
# 参数：
# time_ms - 过期时间（数字毫秒 或 timedelta对象）
r.psetex('fruit3', 1000, 'apple')
print('(7)', r.get('fruit3'))  # apple
time.sleep(1)
print('(7)', r.get('fruit3'))  # 1000毫秒后，取值就从apple变成None

# 8.mset(*args, **kwargs)
# 批量设置值
r.mset({'k1': 'v1', 'k2': 'v2'})  # python3.9好像只能用字典形式
print('(8)', r.mget('k1'))  # ['v1', 'v2']
print('(8)', r.mget('k1', 'k2'))  # ['v1']

# 9.mget(keys, *args)
# 批量获取
r.mget({'k1': 'v1', 'k2': 'v2'})
print('(9)', r.mget('k1', 'k2'))  # ['v1', 'v2']
print('(9)', r.mget(['k1', 'k2']))  # ['v1', 'v2']
print('(9)', r.mget('food', 'fruit', 'fruit1', 'fruit2', 'fruit3', 'k1', 'k2'))  # [None, 'watermelon', 'banana', None, None, 'v1', 'v2']

# 10.getset(name, value)
# 设置新值并获取原来的值，不存在则创建
# r.set('food', 'beef')
print('(10)', r.get('food'))  # None
r.getset('food', 'barbecue')
print('(10)', r.get('food'))  # barbecue

# 11.getrange(key, start, end)
# 获取子序列（根据字节获取，非字符）
# 参数：
# name - Redis 的 name
# start - 起始位置（字节）
# end - 结束位置（字节）
r.set('cn_str', '一二三四五')  # 汉字
print('(11)', r.getrange('cn_str', 0, 2))  # 索引0-2 前3位字节 '一'（1个汉字3个字节，每个字节8bit）
print('(11)', r.getrange('cn_str', 0, -1))  # 一二三四五
r.set('en_str', 'abcde')  # 字母
print('(11)', r.getrange('en_str', 0, 2))  # 索引0-2 前3位字节 'abc'（1个字母1个字节，每个字节8bit）
print('(11)', r.getrange('en_str', 0, -1))  # abcde

# 12.setrange(name, offset, value)
# 修改字符串内容，从指定字符串索引开始向后替换（新值太长时，则向后添加）
# 参数：
# offset - 字符串的索引，字节（一个汉字三个字节）
# value - 要设置的值
r.setrange('en_str', 1, '123')
print('(12)', r.get('en_str'))  # 从索引为1的位置开始依次替换成123 变成 a123e

# 13.setbit(name, offset, value)
# 对 name 对应值的二进制表示的位进行操作
# 参数：
# name - redis的name
# offset - 位的索引（将值变换成二进制后再进行索引）
# value - 值只能是 1 或 0
# 注：如果在Redis中有一个对应： n1 = 'foo'，
# 那么字符串foo的二进制表示为：01100110 01101111 01101111
# 所以，如果执行 setbit('n1', 7, 1)，则就会将第7位设置为1，
# 那么最终二进制则变成 01100111 01101111 01101111，即：'goo'
# 扩展，转换二进制表示：
source = '一二三'
for i in source:
    num = ord(i)
    print('(13)', bin(num))
    # 0b100111000000000
    # 0b100111010001100
    # 0b100111000001001
    print('(13)', bin(num).replace('b', ''))
    # 0100111000000000
    # 0100111010001100
    # 0100111000001001
source = 'abc'
for i in source:
    num = ord(i)
    print('(13)', bin(num))
    # 0b1100001
    # 0b1100010
    # 0b1100011
    print('(13)', bin(num).replace('b', ''))
    # 01100001
    # 01100010
    # 01100011

# 14.getbit(name, offset)
# 获取name对应的值的二进制表示中的某位的值 （0或1）
print('(14)', r.getbit('abcd', 0))  # abcd 对应的二进制 4个字节 32位，输出第0位的数字 0

# 15.bitcount(key, start=None, end=None)
# 获取name对应的值的二进制表示中 1 的个数
# 参数：
# key - Redis的name
# start - 字节起始位置
# end - 字节结束位置
# print(r.get('foo'))  # goo1 01100111
# print(r.bitcount('foo',0,1))  # 11 表示前2个字节中，1出现的个数

# 16.bitop(operation, dest, *keys)
# 获取多个值，并将值做位运算，将最后的结果保存至新的name对应的值
# 参数：
# operation - AND（并） 、 OR（或） 、 NOT（非） 、 XOR（异或）
# dest - 新的Redis的name
# *keys - 要查找的Redis的name
# r.bitop('AND', 'new_name', 'n1', 'n2', 'n3')

# 17.strlen(name)
# 返回name对应值的字节长度（一个汉字3个字节）
# print(r.strlen('foo'))  # 4 'goo1'的长度是4

# 18.incr(self, name, amount=1)
# 自增 name 对应的值，当 name 不存在时，则创建 name＝amount，否则，则自增。
# 参数：
# name - Redis的name
# amount - 自增数（必须是整数）
# 注：同 incrby
# r.set('foo', 123)
# print(r.mget('foo', 'foo1', 'foo2', 'k1', 'k2'))
# r.incr('foo', amount=1)
# print(r.mget('foo', 'foo1', 'foo2', 'k1', 'k2'))

# 19.incrbyfloat(self, name, amount=1.0)
# 自增 name对应的值，当name不存在时，则创建name＝amount，否则，则自增。
# 参数：
# name - Redis的name
# amount - 自增数（浮点型）
r.set('foo1', '123.0')
r.set('foo2', '221.0')
print('(19)', r.mget('foo1', 'foo2'))  # ['123.0', '221.0']
r.incrbyfloat('foo1', amount=2.0)  # 123 + 2
r.incrbyfloat('foo2', amount=3.0)  # 221 + 3
print('(19)', r.mget('foo1', 'foo2'))  # ['125', '224']

# 20.decr(self, name, amount=1)
# 自减 name 对应的值，当 name 不存在时，则创建 name＝amount，否则，则自减。
# 参数：
# name - Redis的name
# amount - 自减数（整数)
r.decr('foo1', amount=1)  # 125 - 1
r.decr('foo2', amount=2)  # 224 - 2
r.decr('foo3', amount=3)  # 0 - 3
print('(20)', r.mget('foo1', 'foo2', 'foo3'))  # ['124', '222', '-3']

# 21.append(key, value)
# 在redis name对应的值后面追加内容
# 参数：
# key - redis的name
# value - 要追加的字符串
r.set('foo4', 'abc')
r.append('foo4', '123')  # 右边追加
print('(21)', r.mget('foo4'))  # ['abc123']
pass


print('\n' + '========== 二、redis基本命令：hash ==========')
# 1、单个增加--修改(单个取出)--没有就新增，有的话就修改
# hset(name, key, value)
# name对应的hash中设置一个键值对（不存在，则创建；否则，修改）
# 参数：
# name - redis的name
# key - name对应的hash中的key
# value - name对应的hash中的value
# 注：hsetnx(name, key, value) 当name对应的hash中不存在当前key时则创建（相当于添加）
r.hset('hash1', 'k1', 'v1')
r.hset('hash1', 'k2', 'v2')
print('(1)', r.hkeys('hash1'))  # ['k1', 'k2'] 取hash中所有的key
print('(1)', r.hget('hash1', 'k1'))  # v1 单个取hash的key对应的值
print('(1)', r.hmget('hash1', 'k1', 'k2'))  # ['v1', 'v2'] 多个取hash的key对应的值
r.hsetnx('hash1', 'k2', 'v3')  # 只能新建，不能修改
print('(1)', r.hget('hash1', 'k2'))  # v2
r.hsetnx('hash1', 'k3', 'v3')  # 只能新建，不能修改
print('(1)', r.hget('hash1', 'k3'))  # v3

# 2、批量增加（取出）
# hmset(name, mapping) 增加
# 在name对应的hash中批量设置键值对
# 参数：
# name - redis的name
# mapping - 字典，如：{'k1':'v1', 'k2': 'v2'}
r.hmset('hash2', {'k1': 'v1', 'k2': 'v2', 'k3': 'v3'})
print('(2)', r.hget('hash2', 'k1'))  # v1
print('(2)', r.hmget('hash2', 'k1', 'k2', 'k3'))  # ['v1', 'v2', 'v3']
# hmget(name, keys, *args) 取出
# 在name对应的hash中获取多个key的值
# 参数：
# name - reids对应的name
# keys - 要获取key集合，如：['k1', 'k2', 'k3']
# *args - 要获取的key，如：k1,k2,k3
print('(2)', r.hmget('hash2', 'k1', 'k2', 'k3'))  # ['v1', 'v2', 'v3'] 方式1
print('(2)', r.hmget('hash2', ['k1', 'k2', 'k3']))  # ['v1', 'v2', 'v3'] 方式2

# 3、取出所有的键值对
# hgetall(name)
# 获取name对应hash的所有键值
print('(3)', r.hgetall('hash1'))  # {'k1': 'v1', 'k2': 'v2', 'k3': 'v3'}

# 4、得到所有键值对的格式 hash长度
# hlen(name)
# 获取name对应的hash中键值对的个数
print('(4)', r.hlen('hash1'))  # 3

# 5、得到所有的keys（类似字典的取所有keys）
# hkeys(name)
# 获取name对应的hash中所有的key的值
print('(5)', r.hkeys('hash1'))  # ['k1', 'k2', 'k3']

# 6、得到所有的value（类似字典的取所有value）
# hvals(name)
# 获取name对应的hash中所有的value的值
print('(6)', r.hvals('hash1'))  # ['v1', 'v2', 'v3']

# 7、判断成员是否存在（类似字典的in）
# hexists(name, key)
# 检查 name 对应的 hash 是否存在当前传入的 key
print('(7)', r.hexists('hash1', 'k1'))  # True 存在
print('(7)', r.hexists('hash1', 'k4'))  # False 不存在

# 8、删除键值对
# hdel(name,*keys)
# 将name对应的hash中指定key的键值对删除
print('(8)', r.hgetall('hash1'))  # {'k1': 'v1', 'k2': 'v2', 'k3': 'v3'}
r.hset('hash1', 'k4', 'v4')  # 新增键值对 k4
print('(8)', r.hgetall('hash1'))  # {'k1': 'v1', 'k2': 'v2', 'k3': 'v3', 'k4': 'v4'}
r.hdel('hash1', 'k4')  # 删除一个键值对
print('(8)', r.hgetall('hash1'))  # {'k1': 'v1', 'k2': 'v2', 'k3': 'v3'}

# 9、自增自减整数(将key对应的value--整数 自增1或者2，或者别的整数 负数就是自减)
# hincrby(name, key, amount=1)
# 自增name对应的hash中的指定key的值，不存在则创建key=amount
# 参数：
# name - redis中的name
# key - hash对应的key
# amount - 自增数（整数）
r.hset('hash1', 'k4', 4)
r.hincrby('hash1', 'k4', amount=-1)  # 减1
print('(9)', r.hgetall('hash1'))  # {'k1': 'v1', 'k2': 'v2', 'k3': 'v3', 'k4': '3'}
r.hincrby('hash1', 'k5', amount=1)  # 不存在该键值对时，新建并默认其value=amount
print('(9)', r.hgetall('hash1'))  # {'k1': 'v1', 'k2': 'v2', 'k3': 'v3', 'k4': '3', 'k5': '1'}

# 10、自增自减浮点数(将key对应的value--浮点数 自增1.0或者2.0，或者别的浮点数 负数就是自减)
# hincrbyfloat(name, key, amount=1.0)
# 自增name对应的hash中的指定key的值，不存在则创建key=amount
# 参数：
# name - redis中的name
# key - hash对应的key
# amount，自增数（浮点数）
# 自增 name 对应的 hash 中的指定 key 的值，不存在则创建 key=amount
r.hset('hash1', 'k5', '1.0')  # 不存在就新建，已存在就修改
r.hincrbyfloat('hash1', 'k5', amount=-1.0)  # 减-1.0
print('(10)', r.hgetall('hash1'))  # {'k5': '0', 'k1': 'v1', 'k2': 'v2', 'k3': 'v3', 'k4': '3'}
r.hincrbyfloat('hash1', 'k6', amount=-1.0)  # 不存在该键值对时，新建并默认其value=amount
print('(10)', r.hgetall('hash1'))  # {'k5': '0', 'k1': 'v1', 'k2': 'v2', 'k3': 'v3', 'k6': '-1', 'k4': '3'}

# 11、取值查看--分片读取
# hscan(name, cursor=0, match=None, count=None)
# 增量式迭代获取，对于数据大的数据非常有用，hscan可以实现分片的获取数据，并非一次性将数据全部获取完，从而放置内存被撑爆
# 参数：
# name - redis的name
# cursor - 游标（基于游标分批取获取数据）
# match - 匹配指定key，默认None 表示所有的key
# count - 每次分片最少获取个数，默认None表示采用Redis的默认分片个数
# 第一次：cursor1, data1 = r.hscan('xx', cursor=0, match=None, count=None)
# 第二次：cursor2, data1 = r.hscan('xx', cursor=cursor1, match=None, count=None)
# 直到返回值cursor的值为0时，表示数据已经通过分片获取完毕
print('(11)', r.hscan('hash1'))  # (0, {'k5': '0', 'k1': 'v1', 'k2': 'v2', 'k3': 'v3', 'k6': '-2', 'k4': '3'})

# 12、hscan_iter(name, match=None, count=None)
# 利用yield封装hscan创建生成器，实现分批去redis中获取数据
# 参数：
# match - 匹配指定key，默认None 表示所有的key
# count - 每次分片最少获取个数，默认None表示采用Redis的默认分片个数
for item in r.hscan_iter('hash1'):
    print('(12)', item)
    # ('k5', '0')
    # ('k1', 'v1')
    # ('k2', 'v2')
    # ('k3', 'v3')
    # ('k6', '-3')
    # ('k4', '3')
print('(12)', r.hscan_iter('hash1'))  # <generator object ScanCommands.hscan_iter at 0x0000011DE1AF6970> 生成器内存地址
pass


print('\n' + '========== 三、redis基本命令：list ==========')
# 1.增加（类似于list的append，只是这里是从左边新增加）--没有就新建
# lpush(name,values)
r.lpush('list1', 1, 11, 111)  # 保存顺序为：111，11，1
print('(1)', r.llen('list1'))  # 输出结果：len(list1) 列表长度
print('(1)', r.lrange('list1', 0, -1))  # 输出结果：[ ... , '111', '11', '1' ] 切片取值，索引0~-1（全部）
print('(1)', r.lrange('list1', 0, 3))  # 输出结果：[ '111', '11', '1', '111' ] 切片取值，索引0~3

# 2.增加（从右边增加）--没有就新建
# rpush(name,values)
r.rpush('list2', 2, 22, 222)
print('(2)', r.llen('list2'))  # 输出结果：len(list2) 列表长度
print('(2)', r.lrange('list2', 0, -1))  # 输出结果：[ '2', '22', '222', ... ] 切片取值，索引0~-1（全部）
print('(2)', r.lrange('list2', 0, 3))  # 输出结果：[ '2', '22', '222', '2' ] 切片取值，索引0~3

# 3.往已经有的name的列表的左边添加元素，没有的话无法创建
# lpushx(name,value)
r.lpushx('list3', 3)  # list3 不存在，无法添加且不新建
print('(3)', r.llen('list3'))  # 0
print('(3)', r.lrange('list3', 0, -1))  # []
r.lpushx('list1', 3)  # list1 存在，可以添加
print('(3)', r.llen('list1'))  # len(list1)
print('(3)', r.lrange('list1', 0, -1))  # [ '3', '111', '11', '1' ]

# 4.往已经有的name的列表的右边添加元素，没有的话无法创建
# rpushx(name,values)
r.rpushx('list4', 4)  # list4 不存在，无法添加且不新建
print('(4)', r.llen('list4'))  # 0
print('(4)', r.lrange('list4', 0, -1))  # []
r.lpushx('list2', 4)  # list2 存在，可以添加
print('(4)', r.llen('list2'))  # len(list2)
print('(4)', r.lrange('list2', 0, -1))  # [ '2', '22', '333', '4' ]

# 5.新增（固定索引号位置插入元素）
# linsert(name, where, refvalue, value))
# 参数：
# name - redis的name
# where - BEFORE或AFTER
# refvalue - 标杆值，即：在它前后插入数据
# value - 要插入的数据
r.linsert('list1', 'before', '11', '5')  # 在第一个11前面插入5
print('(5)', r.lrange('list1', 0, -1))
r.linsert('list2', 'after', '22', '5')  # 在第一个22后面插入6
print('(5)', r.lrange('list2', 0, -1))

# 6.修改（指定索引号进行修改）
# r.lset(name, index, value)
# 参数：
# name - redis的name
# index - list的索引位置
# value - 要设置的值
r.lset('list1', 0, 6)  # 将索引为0的元素修改为6
print('(6)', r.lrange('list1', 0, -1))

# 7.删除（指定值进行删除）
# r.lrem(name, value, num)
# 参数：
# name - redis的name
# value - 要删除的值
# num - num=0，删除列表中所有的指定值；
# num=2 - 从前到后，删除2个, num=1,从前到后，删除左边第1个
# num=-2 - 从后向前，删除2个
r.lrem('list1', 1, 1)  # 将列表中左边第一次出现的11删除
print('(7)', r.lrange('list1', 0, -1))
r.lrem('list1', 11, -1)  # 将列表中右边第一次出现的11删除
print('(7)', r.lrange('list1', 0, -1))
r.lrem('list1', 111, 0)  # 将列表中所有的111删除
print('(7)', r.lrange('list1', 0, -1))

# 8.删除并返回
# lpop(name) 从左向右操作
# rpop(name) 从右向左操作
r.lpop('list2')  # 删除列表最左边的元素，并且返回删除的元素
print('(8)', r.lrange('list2', 0, -1))
r.rpop('list2')  # 删除列表最右边的元素，并且返回删除的元素
print('(8)', r.lrange('list2', 0, -1))

# 9.删除索引之外的值
# ltrim(name, start, end)
# 参数：
# name - redis的name
# start - 索引的起始位置
# end - 索引结束位置
r.ltrim('list2', 0, 2)  # 删除索引号是0-2之外的元素，值保留索引号是0-2的元素
print('(9)', r.lrange('list2', 0, -1))

# 10.取值（根据索引号取值）
# lindex(name, index)
print('(10)', r.lindex('list2', 0))  # 取出索引号是0的值

# 11.移动 元素从一个列表移动到另外一个列表（从一个列表取出最右边的元素，同时将其添加至另一个列表的最左边）
# rpoplpush(src, dst)
# 参数：
# src - 要取数据的列表的 name
# dst - 要添加数据的列表的 name
r.rpoplpush('list1', 'list2')  # 从最右边依次取出 list1 的所有元素，然后依次添加到 list2 的最左边
print('(11)', r.lrange('list2', 0, -1))  # list2 = [ list1, list2 ] 其实就相当于直接把整个 list1 插在 liet2 的最左边

# 12.移动 元素从一个列表移动到另外一个列表 可以设置超时
# brpoplpush(src, dst, timeout=0)
# 参数：
# src - 取出并要移除元素的列表对应的name
# dst - 要插入元素的列表对应的name
# timeout - 当src对应的列表中没有数据时，阻塞等待其有数据的超时时间（秒），0 表示永远阻塞
r.brpoplpush('list1', 'list2', timeout=2)  # 添加方式与上一小节相同
print('(12)', r.lrange('list2', 0, -1))

# 13.一次移除多个列表
# blpop(keys, timeout) 从左向右移除列表中的元素
# brpop(keys, timeout) 从右向左移除列表中的元素
# 参数：
# keys - redis的name的集合
# timeout - 超时时间，当元素所有列表的元素获取完之后，阻塞等待列表内有数据的时间（秒）, 0 表示永远阻塞
r.rpush('list13_1', 1, 2, 3)
r.rpush('list13_2', 4, 5, 6)
while r.llen('list13_2'):
    r.blpop(['list13_1', 'list13_2'], timeout=2)  # 从左向右操作列表，从左向右操作元素
    print('(13)', r.lrange('list13_1', 0, -1), r.lrange('list13_2', 0, -1))
r.rpush('list13_3', 1, 2, 3)
r.rpush('list13_4', 4, 5, 6)
while r.llen('list13_4'):
    r.brpop(['list13_3', 'list13_4'], timeout=2)  # 从左向右操作列表，从右向左操作元素
    print('(13)', r.lrange('list13_3', 0, -1), r.lrange('list13_4', 0, -1))

# 14.自定义增量迭代
# 由于redis类库中没有提供对列表元素的增量迭代，如果想要循环name对应的列表的所有元素，那么就需要获取name对应的所有列表。
# 循环列表
# 但是，如果列表非常大，那么就有可能在第一步时就将程序的内容撑爆，所有有必要自定义一个增量迭代的功能：


def list_iter(name):
    # 自定义redis列表增量迭代
    # :param name: redis中的name，即：迭代name对应的列表
    # :return: yield 返回 列表元素
    list_count = r.llen(name)  # 列表长度
    for index in range(list_count):
        yield r.lindex(name, index)  # 取值


for item in list_iter('list2'):  # 遍历列表
    print('(14)', item)
pass


print('\n' + '========== 四、redis基本命令：无序set ==========')
# 1.新增
# sadd(name,values)
r.sadd('set1', 1, 2, 3, 4)  # 无序添加
print('(1)', r.scard('set1'), r.smembers('set1'))  # 4 {'3', '2', '1', '4'}

# 2.获取元素个数 类似于len
# scard(name)
print('(2)', r.scard('set1'))  # 4

# 3.获取集合中所有的成员--集合形式
# smembers(name)
print('(3)', r.smembers('set1'))  # {'3', '2', '1', '4'}

# 3.获取集合中所有的成员--元组形式
# sscan(name, cursor=0, match=None, count=None)
print('(3)', r.sscan('set1'))  # (0, ['1', '2', '3', '4'])
# 3.获取集合中所有的成员--迭代器的方式
# sscan_iter(name, match=None, count=None)
# 同字符串的操作，用于增量迭代分批获取元素，避免内存消耗太大
for i in r.sscan_iter('set1'):
    print('(3)', i)

# 4.差集 存在于某个集合且不存在于其他集合的这些元素组成的集合，即为差集
# sdiff(keys, *args)
r.sadd('set2', 2, 3, 4, 5)
print('(4)', r.smembers('set1'))
print('(4)', r.smembers('set2'))
print('(4)', r.sdiff('set1', 'set2'))   # 在集合set1但是不在集合set2中
print('(4)', r.sdiff('set2', 'set1'))   # 在集合set2但是不在集合set1中

# 5.差集--将差集存在一个新的集合中
# sdiffstore(dest, keys, *args)
r.sdiffstore('set3', 'set1', 'set2')    # 将存在于集合set1中但是不在集合set2中的所有元素存入集合set3中
r.sdiffstore('set4', 'set2', 'set1')    # 将存在于集合set2中但是不在集合set1中的所有元素存入集合set4中
print('(5)', r.smembers('set3'))
print('(5)', r.smembers('set4'))

# 6.交集
# sinter(keys, *args)
print('(6)', r.sinter('set1', 'set2'))  # 两个集合的交集

# 7.交集--交集存在一个新的集合中
# sinterstore(dest, keys, *args)
r.sinterstore('set5', 'set1', 'set2')  # 将集合set1和集合set2的交集存入集合set5中
print('(7)', r.smembers('set5'))

# 8.并集
# sunion(keys, *args)
print('(8)', r.sunion('set1', 'set2'))  # 两个集合的并集

# 9.并集--并集存在一个新的集合
# sunionstore(dest,keys, *args)
r.sunionstore('set6', 'set1', 'set2')  # 将集合set1和集合set2的并集存入集合set6中
print('(9)', r.smembers('set6'))

# 10.判断某元素是否是某集合的成员 类似于in 结果True或False
# sismember(name, value)
print('(10)', r.sismember('set1', 4))  # True，set1 = {'1', '2', '3', '4'}
print('(10)', r.sismember('set1', 5))  # False

# 11.移动 将某个成员从一个集合中移动到另外一个集合
# smove(src, dst, value)
r.smove('set1', 'set2', 1)  # 将集合set1中的元素移入集合set2中
print('(11)', r.smembers('set1'))  # {'4', '2', '3'}
print('(11)', r.smembers('set2'))  # {'4', '5', '3', '1', '2'}

# 12.删除--随机删除并且返回被删除值
# spop(name)
print('(12)', r.spop('set2'))   # 从无序集合set2中随机删除一个元素
print('(12)', r.smembers('set2'))

# 13.删除--指定值删除
# srem(name, values)
print('(13)', r.srem('set2', 1))   # 指定删除集合set2中的元素 1，若不存在该元素则不改变集合set2
print('(13)', r.smembers('set2'))
pass


print('\n' + '========== 五、redis基本命令：有序set ==========')
# 1.新增
# zadd(name, *args, **kwargs)
r.zadd('z_set1', {'m1': 1, 'm2': 2, 'm3': 3})
print('(1)', r.zcard('z_set1'))  # 2 集合长度
print('(1)', r.zrange('z_set1', 0, -1))  # ['m1', 'm2'] 有序集合中所有元素
print('(1)', r.zrange('z_set1', 0, -1, withscores=True))  # [('m1', 1.0), ('m2', 2.0)] 有序集合中所有元素、分数

# 2.获取有序集合元素个数 类似于len
# zcard(name)
print('(2)', r.zcard('z_set1'))

# 3.获取有序集合的所有元素 按照索引
# zrange( name, start, end, desc=False, withscores=False, score_cast_func=float) 从小到大排序
# zrevrange(name, start, end, withscores=False, score_cast_func=float) 从大到小排序
# 参数：
# name - redis的name
# start - 有序集合索引起始位置（非分数）
# end - 有序集合索引结束位置（非分数）
# desc - 排序规则，默认按照分数从小到大排序
# withscores - 是否获取元素的分数，默认只获取元素的值
# score_cast_func - 对分数进行数据转换的函数
print('(3)', r.zrange('z_set1', 0, -1))
print('(3)', r.zrange('z_set1', 0, -1, withscores=True))  # 从小到大
print('(3)', r.zrevrange('z_set1', 0, -1))
print('(3)', r.zrevrange('z_set1', 0, -1, withscores=True))  # 从大到小

# 4.按照分数范围获取有序集合的元素
# zrangebyscore(name, min, max, start=None, num=None, withscores=False, score_cast_func=float) 从小到大排序
# zrevrangebyscore(name, max, min, start=None, num=None, withscores=False, score_cast_func=float) 从大到小排序
for i in range(1, 10):
    key = 'n' + str(i)
    r.zadd('z_set2', {key: str(i)})
print('(4)', r.zrange('z_set2', 0, -1))
print('(4)', r.zrange('z_set2', 0, -1, withscores=True))
print('(4)', r.zrangebyscore('z_set2', 4, 6))  # 取出value在4到6之间（包含4、6）的元素，根据value从小到大排序
print('(4)', r.zrangebyscore('z_set2', 7, 9, withscores=True))  # 取出value在7到9之间（包含7、9）的元素key、分数value，从小到大
print('(4)', r.zrevrangebyscore('z_set2', 6, 4))  # 取出value在6到4之间（包含6、4）的元素，根据value从大到小排序
print('(4)', r.zrevrangebyscore('z_set2', 9, 7, withscores=True))  # 取出value在9到7之间（包含9、7）的元素key、分数value，从大到小

# 5.获取所有元素--默认按照分数顺序排序
# zscan(name, cursor=0, match=None, count=None, score_cast_func=float)
print('(5)', r.zscan('z_set2'))  # (0, [('n1', 1.0), ('n2', 2.0), ..., ('n8', 8.0), ('n9', 9.0)])

# 6.获取所有元素--迭代器
# zscan_iter(name, match=None, count=None,score_cast_func=float)
for i in r.zscan_iter('z_set2'):  # 遍历迭代器
    print('(6)', i)

# 7.获取有序集合中分数在 [min,max] 之间的元素个数
# zcount(name, min, max)
print('(7)', r.zrange('z_set2', 0, -1, withscores=True))
print('(7)', r.zcount('z_set2', 1, 3))  # 3

# 8.获取值的索引号
# zrank(name, value) 从小到大排序
# zrevrank(name, value) 从大到小排序
print('(8)', r.zrank('z_set2', 'n1'))  # n1的索引为0
print('(8)', r.zrank('z_set2', 'n4'))  # n4的索引为3
print('(8)', r.zrevrank('z_set2', 'n7'))  # n7的索引为6

# 9.删除--指定值删除
# zrem(name, values)
r.zrem('z_set2', 'n1')  # 删除有序集合中的元素n1
print('(9)', r.zrange('z_set2', 0, -1))  # ['n2', 'n3', 'n4', 'n5', 'n6', 'n7', 'n8', 'n9']

# 10.删除--根据索引进行范围删除
# zremrangebyrank(name, min, max)
r.zremrangebyrank('z_set2', 0, 2)  # 删除有序集合中的索引为0到2（包含0、2）的元素
print('(10)', r.zrange('z_set2', 0, -1))  # ['n5', 'n6', 'n7', 'n8', 'n9']

# 11.删除--根据分数进行范围删除
# zremrangebyscore(name, min, max)
r.zremrangebyscore('z_set2', 4, 6)  # 删除有序集合中的分数为4到6（包含4、6）的元素
print('(11)', r.zrange('z_set2', 0, -1))  # ['n7', 'n8', 'n9']

# 12.获取值对应的分数
# zscore(name, value)
print('(12)', r.zscore('z_set2', 'n7'))   # 获取元素n7对应的分数 7.0
pass


print('\n' + '========== 六、其他常用操作 ==========')
# 1.删除
# delete(*names)
# 根据删除redis中的任意数据类型（string、hash、list、set、有序set）
r.set('gender', '男/女')
print('(1)', r.exists('gender'))  # 1
r.delete('gender')  # 删除key为gender的键值对
print('(1)', r.exists('gender'))  # 0

# 2.检查名字是否存在
# exists(name)
# 检测redis的name是否存在，存在就是True，False 不存在
print('(2)', r.exists('z_set1'))  # 1

# 3.模糊匹配
# keys(pattern='')
# 根据模型获取redis的name
# 更多：
# KEYS * 匹配数据库中所有 key 。
# KEYS h?llo 匹配 hello ， hallo 和 hxllo 等。
# KEYS hllo 匹配 hllo 和 heeeeello 等。
# KEYS h[ae]llo 匹配 hello 和 hallo ，但不匹配 hillo
print('(3)', r.keys('foo*'))  # ['foo2', 'fooo', 'foo1', 'foo3', 'food', 'foo', 'foo4', 'food1']

# 4.设置超时时间
# expire(name ,time)
# 为某个redis的某个name设置超时时间
r.lpush('list5', 1, 2, 3)
r.expire('list5', time=1)
print('(4)', r.lrange('list5', 0, -1))  # ['3', '2', '1']
time.sleep(1)
print('(4)', r.lrange('list5', 0, -1))  # []

# 5.重命名
# rename(src, dst)
# 对redis的name重命名
r.lpush('list5', 1, 2, 3)
r.rename('list5', 'list5-1')
print('(5)', r.lrange('list5', 0, -1))  # []
print('(5)', r.lrange('list5-1', 0, -1))  # ['3', '2', '1']


# 6.随机获取name
# randomkey()
# 随机获取一个redis的name（不删除）
print('(6)', r.randomkey())  # set6

# 7.获取类型
# type(name)
# 获取name对应值的类型
print('(7)', r.type('hash1'))  # hsah
print('(7)', r.type('list1'))  # list
print('(7)', r.type('set1'))  # set
print('(7)', r.type('z_set1'))  # zset

# 8.查看所有元素
# scan(cursor=0, match=None, count=None)
print('(8)', r.hscan('hash1'))  # (0, {'k5': '0', 'k1': 'v1', 'k2': 'v2', 'k3': 'v3', 'k6': '-10', 'k4': '3'})
print('(8)', r.sscan('set1'))  # (0, ['2', '3', '4'])
print('(8)', r.zscan('z_set1'))  # (0, [('m1', 1.0), ('m2', 2.0), ('m3', 3.0)])
print('(8)', r.getrange('foo1', 0, -1))  # string 124
print('(8)', r.lrange('list1', 0, -1))  # ['6', '111']
print('(8)', r.smembers('set1'))  # {'4', '2', '3'}
print('(8)', r.zrange('z_set1', 0, -1))  # ['m1', 'm2', 'm3']
print('(8)', r.hgetall('hash1'))  # {'k5': '0', 'k1': 'v1', 'k2': 'v2', 'k3': 'v3', 'k6': '-10', 'k4': '3'}

# 9.查看所有元素--迭代器
# scan_iter(match=None, count=None)
for i in r.hscan_iter('hash1'):
    print('(9)', i)
    # ('k5', '0')
    # ('k1', 'v1')
    # ('k2', 'v2')
    # ('k3', 'v3')
    # ('k6', '-12')
    # ('k4', '3')
for i in r.sscan_iter('set1'):
    print('(9)', i)
    # 2
    # 3
    # 4
for i in r.zscan_iter('z_set1'):
    print('(9)', i)
    # ('m1', 1.0)
    # ('m2', 2.0)
    # ('m3', 3.0)
pass


print('\n' + '========== other方法 ==========')
print(r.get('name'))  # 查询key为name的值 runoob
r.delete('gender')  # 删除key为gender的键值对

print(r.keys())  # 查询所有的数据name ['k2', 'set6', 'set1', 'hash1', 'foo2', 'fruit', 'set4', 'list2', 'foo1', 'z_set2', 'en_str', 'fruit1', 'foo3', 'list1', 'set2', 'z_set1', 'food', 'set5', 'cn_str', 'set3', 'foo4', 'list5-1', 'hash2', 'k1']
print(r.dbsize())  # 当前redis包含多少条数据 24

r.save()  # 执行'检查点'操作，将数据写回磁盘。保存时阻塞

r.flushdb()    # 清空r中的所有数据
print(r.keys())  # []
print(r.dbsize())  # 0
pass

