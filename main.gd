extends Node2D

enum GameState {
	READY,
	PLAYING,
	GAME_OVER,
	WON,
}

@export var fall_limit := 320.0
@export var back_cloud_speed := 8.0
@export var front_cloud_speed := 14.0
@export var cloud_wrap_width := 2200.0

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

func _ready() -> void:
	goal_area.body_entered.connect(_on_goal_body_entered)
	_connect_coins()
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
		_lose()

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
	score = 0
	_reset_coins()
	_reset_player()
	_set_player_active(true)
	_update_hud()
	if start_sfx != null:
		start_sfx.play()
	overlay.hide()

func _restart_game() -> void:
	_start_game()

func _reset_player() -> void:
	player.global_position = spawn_point.global_position
	player.velocity = Vector2.ZERO

	var anim := player.get_node_or_null("AnimatedSprite2D") as AnimatedSprite2D
	if anim != null:
		anim.flip_h = false
		if anim.sprite_frames != null and anim.sprite_frames.has_animation(&"Idle"):
			anim.play(&"Idle")

func _set_player_active(active: bool) -> void:
	player.velocity = Vector2.ZERO
	player.set_physics_process(active)

func _lose() -> void:
	if state != GameState.PLAYING:
		return

	state = GameState.GAME_OVER
	_set_player_active(false)
	_update_hud()
	if lose_sfx != null:
		lose_sfx.play()
	_show_overlay(
		"Game Over",
		"You fell before clearing the course.",
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

func _reset_coins() -> void:
	for coin in get_tree().get_nodes_in_group("coins"):
		coin.reset_coin()

func _on_coin_collected(value: int) -> void:
	score += value
	_update_hud()
	if coin_sfx != null:
		coin_sfx.play()

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
