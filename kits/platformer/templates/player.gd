extends CharacterBody2D

@export var speed := 220.0
@export var jump_velocity := -420.0
@export var gravity := 1200.0

@onready var anim: AnimatedSprite2D = $AnimatedSprite2D
@onready var jump_sfx: AudioStreamPlayer = $JumpSfx

func _physics_process(delta: float) -> void:
	var dir := Input.get_axis("move_left", "move_right")

	if dir > 0:
		anim.flip_h = false
	elif dir < 0:
		anim.flip_h = true

	velocity.x = dir * speed

	if not is_on_floor():
		velocity.y += gravity * delta
		_play_animation(&"Jump")
	else:
		if Input.is_action_just_pressed("jump"):
			velocity.y = jump_velocity
			if jump_sfx != null:
				jump_sfx.play()
			_play_animation(&"Jump")
		elif dir != 0.0:
			_play_animation(&"Run")
		else:
			_play_animation(&"Idle")

	move_and_slide()

func _play_animation(animation_name: StringName) -> void:
	if anim == null or anim.sprite_frames == null:
		return

	if anim.sprite_frames.has_animation(animation_name) and anim.sprite_frames.get_frame_count(animation_name) > 0:
		if anim.animation != animation_name or not anim.is_playing():
			anim.play(animation_name)
		return

	if anim.sprite_frames.has_animation(&"Idle") and anim.sprite_frames.get_frame_count(&"Idle") > 0:
		if anim.animation != &"Idle" or not anim.is_playing():
			anim.play(&"Idle")
