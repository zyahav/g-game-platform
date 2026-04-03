extends Area2D

signal activated(checkpoint: Area2D)

@onready var flag: Polygon2D = $Flag
@onready var glow: Polygon2D = $Glow
@onready var respawn_point: Marker2D = $RespawnPoint

var is_active := false


func _ready() -> void:
	add_to_group("checkpoints")
	body_entered.connect(_on_body_entered)
	_update_visual()


func activate() -> void:
	is_active = true
	_update_visual()


func reset_checkpoint() -> void:
	is_active = false
	_update_visual()


func get_respawn_position() -> Vector2:
	return respawn_point.global_position


func _on_body_entered(body: Node) -> void:
	if body is CharacterBody2D and not is_active:
		activated.emit(self)


func _update_visual() -> void:
	if is_active:
		flag.color = Color(0.207843, 0.788235, 0.364706, 1)
		glow.visible = true
	else:
		flag.color = Color(1, 0.862745, 0.313726, 1)
		glow.visible = false
