/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   source.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oabdelka <oabdelka@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/04/21 17:05:24 by oabdelka          #+#    #+#             */
/*   Updated: 2025/04/21 17:05:25 by oabdelka         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <string.h>


int main() { 
	char input[64];

	printf("please emter the key: ");
	scanf("%63s", input);

	if(strcmp(input, "__stack_check") == 0)
		puts("Good job.");
	else
		puts("NOPE.");

	return 0;
}