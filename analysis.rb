require "pp"
require "rmagick"
require "json"
require_relative "AnimeFace"

image = Magick::ImageList.new(ARGV[0])
faces = AnimeFace::detect(image)
puts faces.to_json