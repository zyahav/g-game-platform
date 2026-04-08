extends Area2D

signal collected(value: int)

@export var value := 1
@export var bob_height := 4.0
@export var bob_speed := 3.5

@onready var collision_shape: CollisionShape2D = $CollisionShape2D

var base_position := Vector2.ZERO
var time_offset := 0.0
var is_collected := false
var pickup_enabled := true

func _ready() -> void:
	add_to_group("coins")
	body_entered.connect(_on_body_entered)
	base_position = position
	time_offset = position.x * 0.01

func _process(_delta: float) -> void:
	if is_collected:
		return

	var t := Time.get_ticks_msec() / 1000.0
	position = base_position + Vector2(0.0, sin(t * bob_speed + time_offset) * bob_height)
	rotation = sin(t * 2.0 + time_offset) * 0.08

func collect() -> void:
	if is_collected:
		return

	is_collected = true
	visible = false
	set_deferred("monitoring", false)
	set_deferred("monitorable", false)
	collision_shape.set_deferred("disabled", true)
	collected.emit(value)

func reset_coin() -> void:
	pickup_enabled = true
	set_collected_state(false)


func set_collected_state(collected_state: bool) -> void:
	is_collected = collected_state
	visible = not collected_state
	rotation = 0.0
	position = base_position
	_sync_pickup_state()


func set_pickup_enabled(enabled: bool) -> void:
	pickup_enabled = enabled
	_sync_pickup_state()


func _sync_pickup_state() -> void:
	var can_pick_up := pickup_enabled and not is_collected
	monitoring = can_pick_up
	monitorable = can_pick_up
	collision_shape.disabled = not can_pick_up

func _on_body_entered(body: Node) -> void:
	if body is CharacterBody2D and pickup_enabled:
		collect()
