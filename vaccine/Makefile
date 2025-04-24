# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: oabdelka <oabdelka@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/04/24 11:42:34 by oabdelka          #+#    #+#              #
#    Updated: 2025/04/24 11:42:36 by oabdelka         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME = vaccine
PYTHON = python3
SRC = vaccine.py
REQ = requirements.txt
LOG = log.txt

all:
	@echo "$(NAME) is ready."

run:
	$(PYTHON) $(SRC)

install:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r $(REQ)

clean:
	rm -f __pycache__/*.pyc 2>/dev/null || true
	rm -rf __pycache__ 2>/dev/null || true
	rm -f storage/*.json 2>/dev/null || true

fclean: clean
	rm -f $(LOG)

re: fclean all