extends GutTest

const MAIN_SCENE := preload("res://Main.tscn")


func _make_main_scene() -> Node:
	return add_child_autofree(MAIN_SCENE.instantiate())


func test_main_scene_instantiates_core_nodes() -> void:
	var main_scene = _make_main_scene()

	assert_not_null(main_scene.get_node_or_null("Player"))
	assert_not_null(main_scene.get_node_or_null("GoalArea"))
	assert_not_null(main_scene.get_node_or_null("CanvasLayer/HUD"))
	assert_not_null(main_scene.get_node_or_null("CanvasLayer/Overlay"))


func test_start_game_sets_playing_state_and_hides_overlay() -> void:
	var main_scene = _make_main_scene()

	main_scene.score = 99
	main_scene._start_game()

	assert_eq(main_scene.state, main_scene.GameState.PLAYING)
	assert_eq(main_scene.score, 0)
	assert_false(main_scene.overlay.visible)
	assert_true(main_scene.player.is_physics_processing())
	assert_eq(main_scene.player.global_position, main_scene.spawn_point.global_position)


func test_coin_collection_updates_score_and_goal_objective() -> void:
	var main_scene = _make_main_scene()

	main_scene._start_game()
	main_scene._on_coin_collected(1)

	assert_eq(main_scene.score, 1)
	assert_string_contains(main_scene.score_label.text, "Score: 1")
	assert_string_contains(main_scene.coins_label.text, "Coins: 1 /")

	main_scene.score = main_scene.total_coins
	main_scene._update_hud()

	assert_eq(main_scene.objective_label.text, "All coins collected - reach the fence")


func test_goal_requires_all_coins_before_winning() -> void:
	var main_scene = _make_main_scene()

	main_scene._start_game()
	main_scene.score = main_scene.total_coins - 1
	main_scene._on_goal_body_entered(main_scene.player)
	assert_eq(main_scene.state, main_scene.GameState.PLAYING)

	main_scene.score = main_scene.total_coins
	main_scene._on_goal_body_entered(main_scene.player)

	assert_eq(main_scene.state, main_scene.GameState.WON)
	assert_true(main_scene.overlay.visible)
	assert_eq(main_scene.objective_label.text, "Course cleared")
	assert_false(main_scene.player.is_physics_processing())


func test_falling_past_limit_triggers_game_over() -> void:
	var main_scene = _make_main_scene()

	main_scene._start_game()
	main_scene.player.global_position.y = main_scene.fall_limit + 10.0
	main_scene._process(0.0)

	assert_eq(main_scene.state, main_scene.GameState.GAME_OVER)
	assert_true(main_scene.overlay.visible)
	assert_eq(main_scene.objective_label.text, "Restart to try again")
	assert_false(main_scene.player.is_physics_processing())
