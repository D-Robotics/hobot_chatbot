from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import TimerAction


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='hobot_llm',
            executable='hobot_llm',
            output='screen',
            parameters=[
                {"topic_sub": "/audio_asr"},
                {"topic_pub": "/tts_text"}
            ],
            arguments=['--ros-args', '--log-level', 'error']
        ),
        TimerAction(
            period=90.0,
            actions=[
                Node(
                    package='hobot_audio',
                    executable='hobot_audio',
                    output='screen',
                    arguments=['--ros-args', '--log-level', 'error']
                ),
                Node(
                    package='hobot_tts',
                    executable='hobot_tts',
                    output='screen',
                    arguments=['--ros-args', '--log-level', 'error']
                )
            ]
        )
    ])
