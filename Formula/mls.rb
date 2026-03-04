class Mls < Formula
  desc "Terminal-native audio/video/image file browser with TUI preview and JSON output"
  homepage "https://github.com/thepushkarp/mls"
  version "0.0.2"
  license "MIT"

  on_macos do
    if Hardware::CPU.arm?
      url "https://github.com/thepushkarp/mls/releases/download/v#{version}/mls-v#{version}-aarch64-apple-darwin.tar.gz"
      sha256 "ebfce47144e7a091baf1861ff98a16d2781a4494060699e0fc4395526f1f3f5e"
    elsif Hardware::CPU.intel?
      url "https://github.com/thepushkarp/mls/releases/download/v#{version}/mls-v#{version}-x86_64-apple-darwin.tar.gz"
      sha256 "7ede35abc687b7a8cb5ddb3ceddc9af6b1b9d9d1adbfcf6b2592c957f9b75ec1"
    end
  end

  depends_on :macos
  depends_on "ffmpeg"

  def install
    bin.install "mls"
  end

  test do
    assert_match "Media LS", shell_output("#{bin}/mls --help")
  end
end
