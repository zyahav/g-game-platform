extends GutTest

const MAIN_SCENE := preload("res://Main.tscn")


func test_main_scene_instantiates_core_nodes() -> void:
	var main_scene = add_child_autofree(MAIN_SCENE.instantiate())

	assert_not_null(main_scene.get_node_or_null("Player"))
	assert_not_null(main_scene.get_node_or_null("GoalArea"))
	assert_not_null(main_scene.get_node_or_null("CanvasLayer/HUD"))
	assert_not_null(main_scene.get_node_or_null("CanvasLayer/Overlay"))
