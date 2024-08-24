#!/bin/bash
export LC_ALL=C
venv=~/cs50_venv
old_path="/Users/franciscoteixeirabarbosa/Dropbox/Classes & Courses/CS50AI 2024 Harvard University/Class II- Knowledge/hands on/Knowledge Inference/cs50"
new_path="/Users/franciscoteixeirabarbosa/cs50_venv"

find "$venv" -type f -exec sed -i '' "s|$old_path|$new_path|g" {} +