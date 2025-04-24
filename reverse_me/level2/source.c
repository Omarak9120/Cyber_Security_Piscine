/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   source.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oabdelka <oabdelka@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/04/21 17:05:18 by oabdelka          #+#    #+#             */
/*   Updated: 2025/04/21 17:15:06 by oabdelka         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <stdlib.h>

void	nopp()
{
	puts("Nope.");
	exit(1);
}

int	yes()
{
	return puts("Good job.");
}

int	main()
{
	char	input[24];
	char	str2[9];
	int		index1;
	int		index2;
	char	num[4];

	printf("Please enter key: ");
	if (scanf("%23s", input) != 1)
		nopp();

	if (input[0] != '0' || input[1] != '0')
		nopp();

	fflush(stdin);
	memset(str2, 0, 9);
	str2[0] = 'd';
	index1 = 2;
	index2 = 1;
	num[3] = '\0';
	while (strlen(str2) < 8 && index1 < (int)strlen(input))
	{
		num[0] = input[index1];
		num[1] = input[index1 + 1];
		num[2] = input[index1 + 2];
		str2[index2] = (char)atoi(num);
		index1 += 3;
		index2 += 1;
	}
	str2[index2] = '\0';

	if (strcmp(str2, "delabere") == 0) {
		yes();
	} else {
		nopp();
	}
	return 0;
}