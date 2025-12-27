package <%= projectNameSnake.downcase %>.app.controllers;

import <%= projectNameSnake.downcase %>.engine.services.LookupsService;
import <%= projectNameSnake.downcase %>.engine.dtos.Lookups;

import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.GetMapping;

@RestController
@RequestMapping("api/lookups")
public class LookupsController {

	private LookupsService lookupsService;

	public LookupsController(LookupsService lookupsService) {
		this.lookupsService = lookupsService;
	}

	@GetMapping
	public Lookups get() {
		return this.lookupsService.getLookups();
	}

}