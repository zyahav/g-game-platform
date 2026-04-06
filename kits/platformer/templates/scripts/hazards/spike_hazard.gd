extends Area2D

signal triggered(body: Node)


func _ready() -> void:
	add_to_group("hazards")
	body_entered.connect(_on_body_entered)


func _on_body_entered(body: Node) -> void:
	triggered.emit(body)
