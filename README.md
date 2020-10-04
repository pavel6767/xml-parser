# Seatmap Availability Exercise:

## About
### Tools
- Python 2.7
- lxml

### Functionality
This is a class that accepts:
- xml source file
- output json file
- reference object for tags used
And outputs a list of seats, split by cabin, with the following structure
```
{
	cabinType: {
		layout: String,
		seats: [
			available: Boolean,
			seatId: _id,
			exitRow: Boolean,
			type: Enumerable(["Window", "Center", "Aisle", "Lavatory"])
			price: String **only if seat is available**
			limitedRecline **only if is limited recline, so few seats are limited recline that makes sense to not make this key required**
		]
	}
}
```

### Possible improvements
- line 8 `self.tagRef`
	- The idea of implementing a tag reference sounds useful for modulatiry
	- I am curious if there is a more efficient way of implementing this
- line 18 `self.namespaces`
	- The variable is hard-coded. Still looking for a way to extract prefix definitions yet
- line 52 `seat_positions = ["Window", "Center", "Aisle"]`
	- Maybe there is a more efficient way, maybe without the list and regex
	- all text content in a `<SeatInfo>` to could filter out `Other_`, leaving the seat type and additional info ("overwing", etc)

## Original Directions

Write a python script that parses the example seatmap response (OTA_AirSeatMapRS.xml) and return a JSON object that lists the seats with the next properties:
- Type (Seat, Kitchen, Bathroom, etc)
- Seat id (17A, 18A)
- Seat price
- Cabin class
- Availability

And any other properties you might find interesting or useful.

The output json format is not defined, so feel free to choose whatever you think best represents the information

