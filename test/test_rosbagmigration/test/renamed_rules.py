class update_test_rosbagmigration_Renamed1_2fbee7c2602a76620804dfad673383b9(MessageUpdateRule):
	old_type = "test_rosbagmigration/Renamed1"
	old_full_text = """
float64  foo  # 2.17
int32[3] bar  # [8, 2, 5]
"""

	new_type = "test_rosbagmigration/Renamed2"
	new_full_text = """
float64  foo  # 2.17
int32[3] bar  # [8, 2, 5]
"""

	order = 0
	migrated_types = []

	valid = True

	def update(self, old_msg, new_msg):
		new_msg.foo = old_msg.foo
		new_msg.bar = old_msg.bar

class update_test_rosbagmigration_Renamed2_2fbee7c2602a76620804dfad673383b9(MessageUpdateRule):
	old_type = "test_rosbagmigration/Renamed2"
	old_full_text = """
float64  foo  # 2.17
int32[3] bar  # [8, 2, 5]
"""

	new_type = "test_rosbagmigration/Renamed3"
	new_full_text = """
float64  foo  # 2.17
int32[4] bar  # [8, 2, 5, 1]
"""

	order = 0
	migrated_types = []

	valid = True

	def update(self, old_msg, new_msg):
                new_msg.foo = old_msg.foo
		new_msg.bar = [old_msg.bar[0], old_msg.bar[1], old_msg.bar[2],  1]

class update_test_rosbagmigration_Renamed3_dd19d6452bb5e45bb900f81fed30ae83(MessageUpdateRule):
	old_type = "test_rosbagmigration/Renamed3"
	old_full_text = """
float64  foo  # 2.17
int32[4] bar  # [8, 2, 5, 1]
"""

	new_type = "test_rosbagmigration/Renamed4"
	new_full_text = """
float64  foo  # 2.17
int32[4] bar  # [8, 2, 5, 1]
"""

	order = 0
	migrated_types = []

	valid = True

	def update(self, old_msg, new_msg):
		new_msg.foo = old_msg.foo
		new_msg.bar = old_msg.bar

