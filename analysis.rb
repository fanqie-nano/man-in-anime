require "pp"
require "rmagick"
require "json"
if RUBY_PLATFORM.include?"darwin18"
	require_relative "mac/AnimeFace"
elsif RUBY_PLATFORM.include?"linux"
	require_relative "linux/AnimeFace"
end

image = Magick::ImageList.new(ARGV[0])
faces = AnimeFace::detect(image)
puts faces.to_json