extends GutTest

const COIN_SCENE := preload("res://scenes/collectibles/Coin.tscn")


func test_collect_hides_coin_and_disables_collision() -> void:
	var coin = add_child_autofree(COIN_SCENE.instantiate())
	var collected_values: Array[int] = []

	coin.collected.connect(func(value: int) -> void:
		collected_values.append(value)
	)

	coin.collect()
	await wait_process_frames(1)

	assert_true(coin.is_collected)
	assert_false(coin.visible)
	assert_false(coin.monitoring)
	assert_false(coin.monitorable)
	assert_true(coin.collision_shape.disabled)
	assert_eq(collected_values, [1])


func test_reset_coin_restores_visibility_and_collision() -> void:
	var coin = add_child_autofree(COIN_SCENE.instantiate())

	coin.collect()
	await wait_process_frames(1)
	coin.reset_coin()
	await wait_process_frames(1)

	assert_false(coin.is_collected)
	assert_true(coin.visible)
	assert_true(coin.monitoring)
	assert_true(coin.monitorable)
	assert_false(coin.collision_shape.disabled)
