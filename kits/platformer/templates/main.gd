extends Node2D

enum GameState {
	READY,
	PLAYING,
	GAME_OVER,
	WON,
}

enum LoseReason {
	FALL,
	HAZARD,
}

@export var fall_limit := 320.0
@export var back_cloud_speed := 8.0
@export var front_cloud_speed := 14.0
@export var cloud_wrap_width := 2200.0
@export var respawn_ground_check_distance := 120.0
@export var respawn_surface_margin := 1.0
@export var debug_spawn_validation := true

@onready var player: CharacterBody2D = $Player
@onready var spawn_point: Marker2D = $SpawnPoint
@onready var goal_area: Area2D = $GoalArea
@onready var overlay: Control = $CanvasLayer/Overlay
@onready var hud: Control = $CanvasLayer/HUD
@onready var score_label: Label = $CanvasLayer/HUD/ScorePanel/MarginContainer/VBoxContainer/ScoreLabel
@onready var coins_label: Label = $CanvasLayer/HUD/ScorePanel/MarginContainer/VBoxContainer/CoinsLabel
@onready var objective_label: Label = $CanvasLayer/HUD/ObjectivePanel/MarginContainer/ObjectiveLabel
@onready var title_label: Label = $CanvasLayer/Overlay/Panel/TitleLabel
@onready var message_label: Label = $CanvasLayer/Overlay/Panel/MessageLabel
@onready var hint_label: Label = $CanvasLayer/Overlay/Panel/HintLabel
@onready var start_sfx: AudioStreamPlayer = $StartSfx
@onready var win_sfx: AudioStreamPlayer = $WinSfx
@onready var lose_sfx: AudioStreamPlayer = $LoseSfx
@onready var coin_sfx: AudioStreamPlayer = $CoinSfx
@onready var back_clouds := [$Background/CloudsBack1, $Background/CloudsBack2, $Background/CloudsBack3]
@onready var front_clouds := [$Background/CloudsFront1, $Background/CloudsFront2, $Background/CloudsFront3]

var state := GameState.READY
var score := 0
var total_coins := 0
var initial_spawn_position := Vector2.ZERO
var respawn_position := Vector2.ZERO
var has_checkpoint := false
var checkpoint_score := 0
var checkpoint_collected_coins: Array[String] = []

func _ready() -> void:
	initial_spawn_position = spawn_point.global_position
	respawn_position = initial_spawn_position
	goal_area.body_entered.connect(_on_goal_body_entered)
	_connect_coins()
	_connect_hazards()
	_connect_checkpoints()
	_clear_checkpoint_state()
	_reset_coins()
	_reset_player()
	_set_player_active(false)
	_update_hud()
	_show_overlay(
		"Warrior Climb",
		"Collect every coin and then reach the fence.",
		"Click anywhere or press Space to start.",
	)

func _process(delta: float) -> void:
	_move_clouds(delta)

	if state == GameState.PLAYING and player.global_position.y > fall_limit:
		_lose(LoseReason.FALL)

func _unhandled_input(event: InputEvent) -> void:
	if state == GameState.PLAYING:
		return

	var mouse_event := event as InputEventMouseButton
	var clicked := mouse_event != null \
		and mouse_event.pressed \
		and mouse_event.button_index == MOUSE_BUTTON_LEFT
	var jumped := event.is_action_pressed("jump")

	if not clicked and not jumped:
		return

	if state == GameState.READY:
		_start_game()
	elif state == GameState.GAME_OVER or state == GameState.WON:
		_restart_game()

func _start_game() -> void:
	state = GameState.PLAYING
	_clear_checkpoint_state()
	score = 0
	_reset_coins()
	_reset_player()
	_set_player_active(true)
	_update_hud()
	if start_sfx != null:
		start_sfx.play()
	overlay.hide()

func _restart_game() -> void:
	if state == GameState.GAME_OVER and has_checkpoint:
		_resume_from_checkpoint()
		return

	_start_game()

func _reset_player() -> void:
	player.global_position = _find_safe_respawn_position(respawn_position)
	player.velocity = Vector2.ZERO

	var anim := player.get_node_or_null("AnimatedSprite2D") as AnimatedSprite2D
	if anim != null:
		anim.flip_h = false
		if anim.sprite_frames != null and anim.sprite_frames.has_animation(&"Idle"):
			anim.play(&"Idle")

func _set_player_active(active: bool) -> void:
	player.velocity = Vector2.ZERO
	player.set_physics_process(active)

func _lose(reason: int = LoseReason.FALL) -> void:
	if state != GameState.PLAYING:
		return

	state = GameState.GAME_OVER
	_set_player_active(false)
	_update_hud()
	if lose_sfx != null:
		lose_sfx.play()
	var lose_message := "You fell before clearing the course."
	if reason == LoseReason.HAZARD:
		lose_message = "You were caught by the spikes before clearing the course."
	_show_overlay(
		"Game Over",
		lose_message,
		"Click anywhere or press Space to restart.",
	)

func _win() -> void:
	if state != GameState.PLAYING:
		return

	state = GameState.WON
	_set_player_active(false)
	_update_hud()
	if win_sfx != null:
		win_sfx.play()
	_show_overlay(
		"You Win",
		"You collected every coin and cleared the climb.",
		"Click anywhere or press Space to play again.",
	)

func _show_overlay(title: String, message: String, hint: String) -> void:
	title_label.text = title
	message_label.text = message
	hint_label.text = hint
	overlay.show()

func _on_goal_body_entered(body: Node) -> void:
	if body == player and score >= total_coins:
		_win()

func _connect_coins() -> void:
	var coins := get_tree().get_nodes_in_group("coins")
	total_coins = coins.size()

	for coin in coins:
		coin.collected.connect(_on_coin_collected)


func _connect_hazards() -> void:
	for hazard in get_tree().get_nodes_in_group("hazards"):
		hazard.triggered.connect(_on_hazard_triggered)


func _connect_checkpoints() -> void:
	for checkpoint in get_tree().get_nodes_in_group("checkpoints"):
		checkpoint.activated.connect(_on_checkpoint_activated)

func _reset_coins() -> void:
	for coin in get_tree().get_nodes_in_group("coins"):
		coin.reset_coin()

func _on_coin_collected(value: int) -> void:
	score += value
	_update_hud()
	if coin_sfx != null:
		coin_sfx.play()


func _on_hazard_triggered(body: Node) -> void:
	if body == player:
		_lose(LoseReason.HAZARD)


func _on_checkpoint_activated(checkpoint: Area2D) -> void:
	for other_checkpoint in get_tree().get_nodes_in_group("checkpoints"):
		other_checkpoint.reset_checkpoint()

	checkpoint.activate()
	has_checkpoint = true
	var checkpoint_position: Vector2 = checkpoint.get_respawn_position()
	respawn_position = _find_safe_respawn_position(checkpoint_position)
	_debug_spawn("checkpoint activated", {
		"checkpoint": checkpoint.name,
		"candidate": checkpoint_position,
		"final_respawn": respawn_position,
	})
	checkpoint_score = score
	checkpoint_collected_coins = _get_collected_coin_names()


func _clear_checkpoint_state() -> void:
	has_checkpoint = false
	respawn_position = initial_spawn_position
	checkpoint_score = 0
	checkpoint_collected_coins.clear()

	for checkpoint in get_tree().get_nodes_in_group("checkpoints"):
		checkpoint.reset_checkpoint()


func _resume_from_checkpoint() -> void:
	state = GameState.PLAYING
	score = checkpoint_score
	_restore_checkpoint_coin_state()
	_reset_player()
	_set_player_active(true)
	_update_hud()
	if start_sfx != null:
		start_sfx.play()
	overlay.hide()


func _get_collected_coin_names() -> Array[String]:
	var names: Array[String] = []

	for coin in get_tree().get_nodes_in_group("coins"):
		if coin.is_collected:
			names.append(coin.name)

	return names


func _restore_checkpoint_coin_state() -> void:
	for coin in get_tree().get_nodes_in_group("coins"):
		coin.set_collected_state(coin.name in checkpoint_collected_coins)


func _find_safe_respawn_position(preferred_position: Vector2) -> Vector2:
	var preferred_safe_position := _safe_position_for(preferred_position)
	if preferred_safe_position != Vector2.INF:
		_debug_spawn("accepted preferred respawn", {
			"candidate": preferred_position,
			"respawn": preferred_safe_position,
		})
		return preferred_safe_position

	var start_safe_position := _safe_position_for(initial_spawn_position)
	if start_safe_position != Vector2.INF:
		_debug_spawn("fallback to level start", {
			"candidate": preferred_position,
			"fallback": initial_spawn_position,
			"respawn": start_safe_position,
		})
		return start_safe_position

	_debug_spawn("forced raw level start fallback", {
		"candidate": preferred_position,
		"fallback": initial_spawn_position,
	})
	return initial_spawn_position


func _safe_position_for(source_position: Vector2) -> Vector2:
	var ground_hit := _find_ground_below(source_position)
	if ground_hit.is_empty():
		_debug_spawn("rejected spawn - no ground hit", {
			"candidate": source_position,
		})
		return Vector2.INF

	var candidate: Vector2 = ground_hit.position
	candidate.y -= _get_player_floor_offset() + respawn_surface_margin

	if _position_overlaps_hazard(candidate):
		_debug_spawn("rejected spawn - hazard overlap", {
			"candidate": source_position,
			"resolved": candidate,
			"ground_hit": ground_hit.position,
		})
		return Vector2.INF

	if _position_overlaps_body(candidate):
		_debug_spawn("rejected spawn - body overlap", {
			"candidate": source_position,
			"resolved": candidate,
			"ground_hit": ground_hit.position,
		})
		return Vector2.INF

	_debug_spawn("validated spawn candidate", {
		"candidate": source_position,
		"ground_hit": ground_hit.position,
		"resolved": candidate,
	})
	return candidate


func _find_ground_below(source_position: Vector2) -> Dictionary:
	var space_state := get_world_2d().direct_space_state
	var query := PhysicsRayQueryParameters2D.create(
		source_position,
		source_position + Vector2(0.0, respawn_ground_check_distance)
	)
	query.collide_with_areas = false
	query.collide_with_bodies = true

	return space_state.intersect_ray(query)


func _get_player_floor_offset() -> float:
	var collision_shape := player.get_node_or_null("CollisionShape2D") as CollisionShape2D
	if collision_shape == null:
		return 20.0

	var rectangle_shape := collision_shape.shape as RectangleShape2D
	if rectangle_shape == null:
		return 20.0

	return collision_shape.position.y + rectangle_shape.size.y * 0.5


func _position_overlaps_hazard(candidate_position: Vector2) -> bool:
	for hazard in get_tree().get_nodes_in_group("hazards"):
		if hazard is Area2D:
			var hazard_shape := hazard.get_node_or_null("CollisionShape2D") as CollisionShape2D
			if hazard_shape == null:
				continue

			var rectangle := hazard_shape.shape as RectangleShape2D
			if rectangle == null:
				continue

			var hazard_center: Vector2 = hazard.global_position + hazard_shape.position
			var half_size := rectangle.size * 0.5
			var hazard_rect := Rect2(hazard_center - half_size, rectangle.size)
			if hazard_rect.has_point(candidate_position):
				return true

	return false


func _position_overlaps_body(candidate_position: Vector2) -> bool:
	var collision_shape := player.get_node_or_null("CollisionShape2D") as CollisionShape2D
	if collision_shape == null:
		return false

	var rectangle_shape := collision_shape.shape as RectangleShape2D
	if rectangle_shape == null:
		return false

	var query := PhysicsShapeQueryParameters2D.new()
	query.shape = rectangle_shape
	query.transform = Transform2D(0.0, candidate_position + collision_shape.position)
	query.collide_with_areas = false
	query.collide_with_bodies = true
	query.margin = 0.0

	var space_state := get_world_2d().direct_space_state
	var collisions := space_state.intersect_shape(query)

	return collisions.size() > 0


func _debug_spawn(label: String, data: Dictionary) -> void:
	if not debug_spawn_validation:
		return

	print("[spawn-debug] %s | %s" % [label, data])

func _update_hud() -> void:
	score_label.text = "Score: %d" % score
	coins_label.text = "Coins: %d / %d" % [score, total_coins]

	if state == GameState.WON:
		objective_label.text = "Course cleared"
	elif state == GameState.GAME_OVER:
		objective_label.text = "Restart to try again"
	elif score >= total_coins and total_coins > 0:
		objective_label.text = "All coins collected - reach the fence"
	else:
		objective_label.text = "Collect all coins to unlock the goal"

	hud.visible = true

func _move_clouds(delta: float) -> void:
	_wrap_clouds(back_clouds, back_cloud_speed * delta)
	_wrap_clouds(front_clouds, front_cloud_speed * delta)

func _wrap_clouds(clouds: Array, step: float) -> void:
	var left_bound := player.global_position.x - 1200.0

	for cloud in clouds:
		cloud.position.x -= step
		if cloud.position.x < left_bound:
			cloud.position.x += cloud_wrap_width
