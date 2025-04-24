/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   source.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oabdelka <oabdelka@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/04/21 18:03:27 by oabdelka          #+#    #+#             */
/*   Updated: 2025/04/21 18:03:28 by oabdelka         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Handle failure
void nopp() {
    puts("Nope.");
    exit(1);
}

// Handle success
void yes() {
    puts("Good job.");
}

int main() {
    char input[31];             // Input buffer for user key
    char decoded[9];            // Final decoded string
    char asciiChunk[4];         // Temporary buffer to hold 3-digit ASCII codes
    int inputIndex = 2;         // Start decoding after the first two characters
    int decodeIndex = 1;        // Start filling from index 1

    printf("Please enter key: ");
    if (scanf("%23s", input) != 1)
		nopp();

    // Check for the "42" prefix
    if (input[0] != '4' || input[1] != '2')
		nopp();

    decoded[0] = '*';           // The first character is hardcoded
    asciiChunk[3] = '\0';       // Null-terminate asciiChunk

    // Decode input into characters
    while (strlen(decoded) < 8 && inputIndex + 2 < strlen(input)) {
        asciiChunk[0] = input[inputIndex];
        asciiChunk[1] = input[inputIndex + 1];
        asciiChunk[2] = input[inputIndex + 2];

        decoded[decodeIndex++] = (char)atoi(asciiChunk);
        inputIndex += 3;
    }

    decoded[decodeIndex] = '\0';  // Null-terminate decoded string

    // Check if decoded string matches the secret
    if (strcmp(decoded, "********") == 0)  // <-- placeholder
		yes();
    else
		nopp();

    return 0;
}
